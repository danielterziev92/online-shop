from datetime import datetime, timedelta

import jwt
from django.test import RequestFactory
from ninja.errors import AuthenticationError

from ecommerce.accounts.mixins.authenticator import JWTAuthenticator
from ecommerce.settings import SECRET_KEY
from tests.base import AppTestCase


class TestJWTAuthenticator(AppTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.factory = RequestFactory()
        cls.auth = JWTAuthenticator()
        cls.account = cls.create_account(is_active=True)

    def test_authenticate__with_valid_token__returns_account(self):
        token = jwt.encode(
            {'account_id': self.account.id, 'exp': datetime.utcnow() + timedelta(days=1)},
            SECRET_KEY, algorithm='HS256'
        )

        request = self.factory.get('/api/account')

        result = self.auth.authenticate(request, token)

        self.assertEqual(result, self.account)

    def test_authenticate__with_expired_token__raises_error(self):
        token = jwt.encode(
            {'account_id': self.account.id, 'exp': datetime.utcnow() - timedelta(days=1)},
            SECRET_KEY, algorithm='HS256'
        )
        request = self.factory.get('/api/account')

        with self.assertRaisesMessage(AuthenticationError, 'Token has expired'):
            self.auth.authenticate(request, token)

    def test_authenticate__with_invalid_token__raises_error(self):
        request = self.factory.get('/api/account')

        with self.assertRaisesMessage(AuthenticationError, 'Invalid token'):
            self.auth.authenticate(request, 'invalid.token.here')

    def test_authenticate__with_no_token__raises_error(self):
        request = self.factory.get('/api/account')

        with self.assertRaisesMessage(AuthenticationError, 'Token is required'):
            self.auth.authenticate(request, None)

    def test_authenticate__with_inactive_account__raises_error(self):
        inactive_account = self.create_account(email='inactive@example.com', is_active=False)
        token = jwt.encode(
            {'account_id': inactive_account.id, 'exp': datetime.utcnow() + timedelta(days=1)},
            SECRET_KEY, algorithm='HS256'
        )
        request = self.factory.get('/api/account')

        with self.assertRaisesMessage(AuthenticationError, 'User not found or inactive'):
            self.auth.authenticate(request, token)

    def test_authenticate__with_nonexistent_account_id__raises_error(self):
        token = jwt.encode(
            {'account_id': 99999, 'exp': datetime.utcnow() + timedelta(days=1)},
            SECRET_KEY, algorithm='HS256'
        )
        request = self.factory.get('/api/account')

        with self.assertRaisesMessage(AuthenticationError, 'User not found or inactive'):
            self.auth.authenticate(request, token)
