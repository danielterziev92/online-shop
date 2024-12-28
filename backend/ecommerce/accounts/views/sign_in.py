from django.contrib.auth import authenticate
from ninja import Router
from ninja.responses import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ecommerce.accounts.mixins.token_utils import TokenUtilsMixin
from ecommerce.accounts.schemas import TokenSchema, SignInErrorSchema, SignInSchema, AuthErrors

sign_in_router = Router()


@sign_in_router.post(
    'sign-in/',
    response={status.HTTP_200_OK: TokenSchema, status.HTTP_401_UNAUTHORIZED: SignInErrorSchema},
    auth=None,
    description="Signs in account and returns access token in response and refresh token in cookie",
    summary="Account sign in",
    tags=["Authentication"]
)
def sign_in(request, data: SignInSchema):
    account = authenticate(email=data.email, password=data.password)

    if not account:
        return status.HTTP_401_UNAUTHORIZED, {'error': AuthErrors.INVALID_CREDENTIALS}

    if not account.is_active:
        return status.HTTP_401_UNAUTHORIZED, {'error': AuthErrors.ACCOUNT_NOT_ACTIVE}

    refresh = RefreshToken.for_user(account)
    response = Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    TokenUtilsMixin.set_auth_cookie(response=response, token_name='token', token=str(refresh))

    return response
