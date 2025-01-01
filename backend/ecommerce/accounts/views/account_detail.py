from ninja import Router, Schema

from ecommerce.accounts.mixins.authenticator import JWTAuthenticator
from ecommerce.accounts.models import BaseAccount
from ecommerce.utilities import status

account_detail_router = Router()


class AccountResponseSchema(Schema):
    email: str
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True


@account_detail_router.get(
    'account/detail/',
    response={status.HTTP_200_OK: AccountResponseSchema},
    auth=JWTAuthenticator(),
    description='Get authenticated user information',
    summary='',
    tags=['Authentication']
)
def account_detail(request):
    account: BaseAccount = request.auth

    account_data = {'email': account.email, 'is_active': account.is_active, 'is_staff': account.is_staff}
    return status.HTTP_200_OK, account_data
