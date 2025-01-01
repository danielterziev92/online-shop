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
