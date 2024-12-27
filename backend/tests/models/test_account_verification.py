from django.db import transaction
from django.utils import timezone

from ecommerce.accounts.models import AccountVerification, BaseAccount
from tests.base import AppTestCase


class TestAccountVerification(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.account = cls.create_account()

    def test_create_verification__when_valid_data__expect_success(self):
        verification = AccountVerification.objects.create(account=self.account)

        self.assertEqual(len(verification.verification_code), AccountVerification.VERIFICATION_MAX_LENGTH)
        self.assertGreater(verification.expiration_time, timezone.now())

    def test_is_expired__when_time_passed__expect_true(self):
        verification = AccountVerification.objects.create(account=self.account)
        verification.expiration_time = timezone.now() - timezone.timedelta(hours=2)
        verification.save()

        self.assertTrue(verification.is_expired)

    def test_is_expired__when_time_not_passed__expect_false(self):
        verification = AccountVerification.objects.create(account=self.account)

        self.assertFalse(verification.is_expired)

    def test_save__when_concurrent_saves__expect_unique_codes(self):
        with transaction.atomic():
            verification1 = AccountVerification.objects.create(account=self.account)
            verification2 = AccountVerification.objects.create(
                account=BaseAccount.objects.create()
            )

        self.assertNotEqual(verification1.verification_code, verification2.verification_code)
