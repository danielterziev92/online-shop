from django.contrib.auth import authenticate
from ninja import Router
from ninja.responses import Response

from ecommerce.accounts.mixins.token_utils import TokenUtilsMixin
from ecommerce.accounts.models import BaseAccount
from ecommerce.accounts.schemas import TokenSchema, SignInErrorSchema, SignInSchema, AuthErrors
from ecommerce.utilities import status

sign_in_router = Router()


@sign_in_router.post(
    'sign-in/',
    response={status.HTTP_200_OK: TokenSchema, status.HTTP_401_UNAUTHORIZED: SignInErrorSchema},
    auth=None,
    description='Signs in account and returns access token in response and refresh token in cookie',
    summary='Account sign in',
    tags=['Authentication']
)
def sign_in(request, data: SignInSchema):
    account: BaseAccount | None = authenticate(email=data.email, password=data.password)

    if not account:
        return status.HTTP_401_UNAUTHORIZED, {'error': AuthErrors.INVALID_CREDENTIALS}

    if not account.is_active:
        return status.HTTP_401_UNAUTHORIZED, {'error': AuthErrors.ACCOUNT_NOT_ACTIVE}

    access, refresh = TokenUtilsMixin().create_tokens(account)
    response = Response({'token': access}, status=status.HTTP_200_OK)
    TokenUtilsMixin.set_auth_cookie(response=response, token_name='token', token=refresh)
    return response
