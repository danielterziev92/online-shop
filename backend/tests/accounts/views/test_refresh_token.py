import json

import jwt
from django.utils import timezone

from ecommerce.accounts.mixins.token_utils import TokenUtilsMixin
from ecommerce.settings import JWT_SETTINGS
from ecommerce.utilities import status
from tests.base import AppTestCase


class TestRefreshToken(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.account = cls.create_account(is_active=True)
        cls.utils = TokenUtilsMixin()
        cls.refresh_token = cls.utils.create_refresh_token(cls.account)

    def setUp(self):
        self.client.cookies['token'] = self.refresh_token

    def test_refresh_token__with_valid_refresh_token__returns_new_tokens(self):
        response = self.client.post('/api/auth/refresh/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'token', response.content)
        self.assertIn('token', response.cookies)

        token = json.loads(response.content.decode())['token']
        is_expired, payload = self.utils.validate_token(token)
        self.assertFalse(is_expired)
        self.assertEqual(payload['account_id'], self.account.id)

    def test_refresh_token__without_refresh_token__returns_401(self):
        self.client.cookies.pop('token')
        response = self.client.post('/api/auth/refresh/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content.decode())['error'], 'Refresh token is required.')

    def test_refresh_token__with_expired_token__returns_401(self):
        expired_payload = {
            'account_id': self.account.id,
            'is_verified': self.account.is_active,
            'exp': timezone.now().timestamp() - 1
        }
        expired_token = jwt.encode(expired_payload, JWT_SETTINGS['SECRET_KEY'], algorithm=JWT_SETTINGS['ALGORITHM'])
        self.client.cookies['token'] = expired_token

        response = self.client.post('/api/auth/refresh/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content.decode())['error'], 'Token has expired')

    def test_refresh_token__with_invalid_account_id__returns_401(self):
        payload = {
            'account_id': 99999,
            'is_verified': True,
            'exp': (timezone.now() + JWT_SETTINGS['REFRESH_TOKEN_LIFETIME']).timestamp()
        }
        token = jwt.encode(payload, JWT_SETTINGS['SECRET_KEY'], algorithm=JWT_SETTINGS['ALGORITHM'])
        self.client.cookies['token'] = token

        response = self.client.post('/api/auth/refresh/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content.decode())['error'], 'Invalid token')
