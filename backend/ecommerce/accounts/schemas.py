from dataclasses import dataclass

from ninja import Schema, Field


class TokenSchema(Schema):
    """
    Returns access token in response body, refresh token set in HTTP Only cookie.
    """
    token: str


@dataclass(frozen=True)
class AuthErrors:
    INVALID_CREDENTIALS: str = 'Invalid credentials'
    ACCOUNT_NOT_ACTIVE: str = 'Account is not activated'
    INVALID_TOKEN: str = 'Invalid token'
    TOKEN_EXPIRED: str = 'Token has expired'
    PASSWORD_MISMATCH: str = 'Passwords do not match'
    TERMS_CONFORMATION: str = 'Terms must be accepted'
    EMAIL_EXISTS: str = 'Email already exists'
    CODE_REQUIRED: str = 'Code is required'
    CODE_NOT_EXIST: str = 'Code does not exist'


class SignInErrorSchema(Schema):
    """
    Authentication Error Responses:
    - 401:
        - Invalid credentials
        - Account not activated
    """
    error: str = Field(
        ...,
        description='Error message',
        example=AuthErrors.INVALID_CREDENTIALS
    )


class SignInSchema(Schema):
    email: str
    password: str


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


class VerifyCodeErrorSchema(Schema):
    """
    Error Responses:
    - 400:
    """
    error: str = Field(
        ...,
        description='Error message',
        examples=AuthErrors.PASSWORD_MISMATCH,
    )


class VerifyCodeSchema(Schema):
    code: str
