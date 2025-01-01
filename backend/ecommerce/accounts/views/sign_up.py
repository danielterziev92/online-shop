from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ninja import Router, Schema, Field

from ecommerce.accounts.models import BaseAccount
from ecommerce.accounts.schemas import AuthErrors
from ecommerce.utilities import status

sign_up_router = Router()

AccountModel: BaseAccount = get_user_model()


class SignUpErrorSchema(Schema):
    """
    Error Responses:
    - 400:
        - Passwords do not match
        - Terms must be accepted
        - Email already exists
    """
    error: str = Field(
        ...,
        description='Error message',
        example=AuthErrors.PASSWORD_MISMATCH,
    )


class SignUpSchema(Schema):
    email: str
    password: str
    repeatPassword: str
    terms: bool


@sign_up_router.post(
    'sign-up/',
    response={status.HTTP_201_CREATED: dict, status.HTTP_400_BAD_REQUEST: SignUpErrorSchema},
    auth=None,
    description='Creates an inactive account pending email verification. Validates password strength, confirms password match, and requires terms acceptance.',
    summary='Create new account',
    tags=['Authentication']
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
