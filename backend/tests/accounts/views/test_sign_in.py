from tests.base import AppTestCase


class TestSignIn(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.url = '/api/auth/sign-in/'
        cls.email = 'test@test.bg'
        cls.password = 'P@ssword1'
        cls.account = cls.create_account(email=cls.email, password=cls.password, is_active=True)

    def test_sign_in__when_valid_credentials__expect_tokens_and_cookie(self):
        response = self.client.post(
            self.url,
            {'email': self.email, 'password': self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertIn('token', response.cookies)

    def test_sign_in__when_invalid_credentials__expect_401(self):
        response = self.client.post(
            self.url,
            {'email': self.email, 'password': 'wrong'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_sign_in__when_inactive_account__expect_401(self):
        self.account.is_active = False
        self.account.save()

        response = self.client.post(
            self.url,
            {'email': self.email, 'password': self.password},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)
