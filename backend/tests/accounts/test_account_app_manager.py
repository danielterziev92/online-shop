from tests.base import AppTestCase


class TestAccountAppManager(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.account_valid_data = {'email': 'test@email.com', 'password': 'P@ssword1'}

    def test_create_account_no_active__with_valid_credentials__creates_inactive_user(self):
        account = self.AccountModel.objects.create_account_no_active(**self.account_valid_data)

        self.assertEqual(account.email, self.account_valid_data['email'])
        self.assertFalse(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_create_account_active__with_valid_credentials__creates_active_user(self):
        account = self.AccountModel.objects.create_account_active(**self.account_valid_data)

        self.assertEqual(account.email, self.account_valid_data['email'])
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_create_superuser__with_valid_credentials__creates_superuser(self):
        account = self.AccountModel.objects.create_superuser(**self.account_valid_data)

        self.assertEqual(account.email, self.account_valid_data['email'])
        self.assertTrue(account.is_active)
        self.assertTrue(account.is_staff)
        self.assertTrue(account.is_superuser)

    def test_create_account__with_empty_email__raises_value_error(self):
        with self.assertRaisesMessage(ValueError, 'Email required'):
            self.AccountModel.objects.create_account_no_active('', self.account_valid_data['password'])

        with self.assertRaisesMessage(ValueError, 'Email required'):
            self.AccountModel.objects.create_account_active('', self.account_valid_data['password'])

    def test_create_user__with_uppercase_email__normalizes_email(self):
        account = self.AccountModel.objects.create_account_no_active('TEST@test.com', 'P@ssword1')
        self.assertEqual(account.email, 'TEST@test.com')
