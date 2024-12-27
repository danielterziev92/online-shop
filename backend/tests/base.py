from django.contrib.auth import get_user_model
from django.test import TestCase

from ecommerce.accounts.models import BaseAccount


class AppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.AccountModel: BaseAccount = get_user_model()

    def setUp(self) -> None:
        print(f'Test Started: {self._testMethodName}')

    @classmethod
    def create_account(cls, email: str = 'test@email.com', password: str = 'P@ssowrd1',
                       is_active: bool = False) -> BaseAccount:
        model = cls.AccountModel
        creator = model.objects.create_account_active if is_active else model.objects.create_account_no_active
        return creator(email=email, password=password)
