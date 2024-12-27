from django.contrib.auth import base_user
from django.contrib.auth.hashers import make_password


class AccountAppManager(base_user.BaseUserManager):
    use_in_migrations = True

    def create_account_no_active(self, email, password=None, **extra_fields):
        return self._create_user(
            email,
            password,
            **{**self._prepare_fields(), **extra_fields}
        )

    def create_account_active(self, email, password=None, **extra_fields):
        return self._create_user(
            email,
            password,
            **{**self._prepare_fields(is_active=True), **extra_fields}
        )

    def create_superuser(self, email, password=None, **extra_fields):
        fields = self._prepare_fields(True, True, True)
        if not all(fields.values()):
            raise ValueError('Superuser requires all permissions')
        return self._create_user(email, password, **{**fields, **extra_fields})

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email required')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    @staticmethod
    def _prepare_fields(is_staff=False, is_superuser=False, is_active=False):
        return {
            'is_staff': is_staff,
            'is_superuser': is_superuser,
            'is_active': is_active
        }
