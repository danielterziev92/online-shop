from django.contrib.auth import get_user_model
from ninja import Router, Schema
from ninja.responses import Response
from ninja.schema import Field

from ecommerce.accounts.mixins.authenticator import JWTAuthenticator
from ecommerce.accounts.mixins.token_utils import TokenUtilsMixin
from ecommerce.accounts.schemas import TokenSchema
from ecommerce.utilities import status

refresh_token_router = Router()

AccountModel = get_user_model()


class ErrorSchema(Schema):
    error: str = Field(description='Error message details')


@refresh_token_router.post(
    'refresh/',
    response={status.HTTP_200_OK: TokenSchema, status.HTTP_401_UNAUTHORIZED: ErrorSchema},
    auth=None,
    description='Refresh access token using refresh token',
    summary='Refresh tokens',
    tags=['Authentication'],
)
def refresh_token(request):
    refresh_token = request.COOKIES.get('token')
    if not refresh_token:
        return status.HTTP_401_UNAUTHORIZED, {'error': 'Refresh token is required.'}

    utils = TokenUtilsMixin()

    is_expired, payload = utils.validate_token(refresh_token)
    if is_expired:
        return status.HTTP_401_UNAUTHORIZED, {'error': 'Token has expired'}

    try:
        account = AccountModel.objects.get(id=payload['account_id'])
        access, refresh = utils.create_tokens(account=account)
        response = Response({'token': access}, status=status.HTTP_200_OK)
        TokenUtilsMixin.set_auth_cookie(response=response, token_name='token', token=refresh)
        return response
    except AccountModel.DoesNotExist:
        return status.HTTP_401_UNAUTHORIZED, {'error': 'Invalid token'}
