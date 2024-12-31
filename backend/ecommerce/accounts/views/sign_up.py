from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from ninja import Router
from pydantic import ValidationError

from ecommerce.accounts.models import BaseAccount
from ecommerce.accounts.schemas import SignUpErrorSchema, SignUpSchema, AuthErrors
from ecommerce.utilities import status

sign_up_router = Router()

AccountModel: BaseAccount = get_user_model()


@sign_up_router.post(
    'sign-up/',
    response={status.HTTP_201_CREATED: dict, status.HTTP_401_UNAUTHORIZED: SignUpErrorSchema},
    auth=None,
    description="Signs in account and returns access token in response and refresh token in cookie",
    summary="Account sign in",
    tags=["Authentication"]
)
def sign_up(request, data: SignUpSchema):
    if data.password != data.repeatPassword:
        return status.HTTP_400_BAD_REQUEST, {'error': AuthErrors.PASSWORD_MISMATCH}

    if not data.terms:
        return status.HTTP_400_BAD_REQUEST, {'error': AuthErrors.TERMS_CONFORMATION}

    try:
        validate_password(data.password)
    except ValidationError as e:
        return status.HTTP_400_BAD_REQUEST, {'error': str(e)}

    try:
        AccountModel.objects.create_account_no_active(email=data.email, password=data.password)
        return status.HTTP_201_CREATED, {'message': 'Account created successfully'}
    except IntegrityError:
        return status.HTTP_400_BAD_REQUEST, {'error': AuthErrors.EMAIL_EXISTS}
