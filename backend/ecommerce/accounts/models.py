from random import choices
from string import digits

from django.db import models, transaction
from django.contrib.auth import models as auth_models
from django.utils import timezone

from ecommerce.accounts.manager import AccountAppManager
from ecommerce.utilities.model_mixins import TimeStampModel


class BaseAccount(auth_models.AbstractBaseUser, auth_models.PermissionsMixin, TimeStampModel):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    is_active = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    objects = AccountAppManager()

    class Meta:
        db_table = 'base_account'
        indexes = (
            models.Index(fields=('email',)),
        )

    def __str__(self):
        return self.email


class AccountVerification(models.Model):
    VERIFICATION_MAX_LENGTH = 6

    verification_code = models.CharField(
        max_length=VERIFICATION_MAX_LENGTH,
        unique=True,
        null=False,
        blank=False,
    )

    expiration_time = models.DateTimeField()

    account = models.OneToOneField(
        to=BaseAccount,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='verification',
    )

    @property
    def is_expired(self):
        return timezone.now() > self.expiration_time

    @classmethod
    def __generate_unique_verification_code(cls):
        return ''.join(choices(digits, k=cls.VERIFICATION_MAX_LENGTH))

    class Meta:
        db_table = 'account_verification'
        indexes = (
            models.Index(fields=('verification_code',)),
        )

    def save(self, *args, **kwargs):
        if not self.verification_code:
            with transaction.atomic():
                AccountVerification.objects.select_for_update().filter(verification_code__isnull=False).exists()

                while True:
                    code = self.__generate_unique_verification_code()
                    if not AccountVerification.objects.filter(verification_code=code).exists():
                        self.verification_code = code
                        self.expiration_time = timezone.now() + timezone.timedelta(hours=1)
                        break
        super().save(*args, **kwargs)
