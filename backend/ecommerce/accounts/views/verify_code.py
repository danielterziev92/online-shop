from ninja import Router
from ninja.responses import Response

from ecommerce.accounts.mixins.token_utils import TokenUtilsMixin
from ecommerce.accounts.models import AccountVerification
from ecommerce.accounts.schemas import TokenSchema, VerifyCodeErrorSchema, VerifyCodeSchema, AuthErrors
from ecommerce.utilities import status

verify_code_router = Router()


@verify_code_router.post(
    'verify/',
    response={status.HTTP_200_OK: TokenSchema, status.HTTP_400_BAD_REQUEST: VerifyCodeErrorSchema},
    auth=None,
    description='',
    summary='',
    tags=['Authentication']
)
def verify_code(request, data: VerifyCodeSchema):
    if not data.code:
        return status.HTTP_400_BAD_REQUEST, {'error': AuthErrors.CODE_REQUIRED}

    try:
        verification = AccountVerification.objects.get(verification_code=data.code)
        account = verification.account
        account.is_active = True
        account.save()

        access, refresh = TokenUtilsMixin().create_tokens(account)
        response = Response({'token': access}, status=status.HTTP_200_OK)
        TokenUtilsMixin.set_auth_cookie(response=response, token_name='token', token=refresh)
        return response

    except AccountVerification.DoesNotExist:
        return status.HTTP_400_BAD_REQUEST, {'error': AuthErrors.CODE_NOT_EXIST}
