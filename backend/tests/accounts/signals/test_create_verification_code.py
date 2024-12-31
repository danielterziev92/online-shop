from unittest.mock import patch

from ecommerce.accounts.models import BaseAccount, AccountVerification
from tests.base import AppTestCase


class TestAccountVerification(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    @patch('ecommerce.accounts.tasks.send_verification_email.send')
    def test_create_verification_code__when_user_created__creates_verification_and_sends_email(self, mock_send):
        account: BaseAccount = self.create_account()
        account_verification = AccountVerification.objects.filter(account=account).first()

        self.assertIsNotNone(account_verification.verification_code)
        mock_send.assert_called_once_with(account.email, account_verification.verification_code)

    @patch('ecommerce.accounts.tasks.send_verification_email.send')
    def test_create_verification_code__when_user_updated__does_not_send_email(self, mock_send):
        account = self.create_account()
        mock_send.reset_mock()

        account.save()
        mock_send.assert_not_called()
