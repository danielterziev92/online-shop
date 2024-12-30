import jwt
from django.utils import timezone
from ninja.responses import Response

from ecommerce.accounts.mixins.token_utils import TokenUtilsMixin
from ecommerce.settings import JWT_SETTINGS
from tests.base import AppTestCase


class TestTokenUtilsMixin(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.mixin = TokenUtilsMixin()
        cls.account = cls.create_account(is_active=True)
        cls.response = Response({})

    def test_set_auth_cookie__with_valid_inputs__sets_cookie_with_correct_params(self):
        token = "test_token"
        token_name = "access_token"

        self.mixin.set_auth_cookie(self.response, token_name, token)

        self.assertEqual(self.response.cookies[token_name].value, token)
        self.assertTrue(self.response.cookies[token_name]['httponly'])
        self.assertEqual(self.response.cookies[token_name]['samesite'], 'Lax')
        self.assertTrue(self.response.cookies[token_name]['secure'])
        self.assertEqual(self.response.cookies[token_name]['max-age'], JWT_SETTINGS['COOKIE_MAX_AGE'].total_seconds())

    def test_create_tokens__with_valid_account__returns_access_and_refresh_tokens(self):
        access_token, refresh_token = self.mixin.create_tokens(self.account)

        payload = jwt.decode(access_token, JWT_SETTINGS['SECRET_KEY'], algorithms=[JWT_SETTINGS['ALGORITHM']])
        self.assertEqual(payload['account_id'], self.account.pk)
        self.assertEqual(payload['is_verified'], self.account.is_active)

        payload = jwt.decode(refresh_token, JWT_SETTINGS['SECRET_KEY'], algorithms=[JWT_SETTINGS['ALGORITHM']])
        self.assertEqual(payload['account_id'], self.account.pk)
        self.assertEqual(payload['is_verified'], self.account.is_active)

    def test_create_access_token__with_valid_account__returns_valid_jwt(self):
        token = self.mixin.create_access_token(self.account)
        payload = jwt.decode(token, JWT_SETTINGS['SECRET_KEY'], algorithms=[JWT_SETTINGS['ALGORITHM']])

        self.assertEqual(payload['account_id'], self.account.pk)
        self.assertEqual(payload['is_verified'], self.account.is_active)
        self.assertAlmostEqual(
            payload['exp'],
            (timezone.now() + JWT_SETTINGS['ACCESS_TOKEN_LIFETIME']).timestamp(),
            delta=1
        )

    def test_create_refresh_token__with_valid_account__returns_valid_jwt(self):
        token = self.mixin.create_refresh_token(self.account)
        payload = jwt.decode(token, JWT_SETTINGS['SECRET_KEY'], algorithms=[JWT_SETTINGS['ALGORITHM']])

        self.assertEqual(payload['account_id'], self.account.pk)
        self.assertEqual(payload['is_verified'], self.account.is_active)
        self.assertAlmostEqual(
            payload['exp'],
            (timezone.now() + JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']).timestamp(),
            delta=1
        )
