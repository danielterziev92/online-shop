from django.db import models
from django.contrib.auth import models as auth_models

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
