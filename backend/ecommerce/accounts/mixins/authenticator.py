from typing import Optional

import jwt
from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
from ninja.security import HttpBearer

from ecommerce.settings import SECRET_KEY

Account = get_user_model()


class JWTAuthenticator(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[Account]:
        if not token:
            raise AuthenticationError('Token is required')

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=['HS256'],
                options={"verify_exp": True}
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationError('Invalid token')

        try:
            account = Account.objects.get(id=payload['account_id'], is_active=True)
        except Account.DoesNotExist:
            raise AuthenticationError('User not found or inactive')

        return account
