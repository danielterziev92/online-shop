import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone
from ninja.responses import Response

from ecommerce.settings import JWT_SETTINGS

AccountModel = get_user_model()


class TokenUtilsMixin:
    @staticmethod
    def set_auth_cookie(response: Response, token_name: str, token: str) -> None:
        return response.set_cookie(
            token_name, token, httponly=True, samesite='Lax', secure=True, max_age=JWT_SETTINGS['COOKIE_MAX_AGE']
        )

    def create_tokens(self, account: AccountModel) -> tuple:
        return self.__create_token(account, 'access'), self.__create_token(account, 'refresh')

    @staticmethod
    def create_access_token(account: AccountModel) -> jwt.encode:
        return TokenUtilsMixin.__create_token(account, 'access')

    @staticmethod
    def create_refresh_token(account: AccountModel) -> jwt.encode:
        return TokenUtilsMixin.__create_token(account, 'refresh')

    @staticmethod
    def validate_token(token: str) -> tuple[bool, dict | None]:
        try:
            payload = jwt.decode(token, JWT_SETTINGS['SECRET_KEY'], algorithms=JWT_SETTINGS['ALGORITHM'])
            exp_datetime = timezone.make_aware(timezone.datetime.fromtimestamp(payload['exp']))
            return timezone.now() >= exp_datetime, payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
            return True, None

    @staticmethod
    def __create_token(account: AccountModel, token_type: str) -> jwt.encode:
        return jwt.encode(
            {
                'account_id': account.pk,
                'is_verified': account.is_active,
                'exp': timezone.now() + JWT_SETTINGS[f'{token_type.upper()}_TOKEN_LIFETIME']
            },
            JWT_SETTINGS['SECRET_KEY'],
            algorithm=JWT_SETTINGS['ALGORITHM']
        )
