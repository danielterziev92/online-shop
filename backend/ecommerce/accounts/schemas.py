from dataclasses import dataclass

from ninja import Schema, Field


class TokenSchema(Schema):
    """
    Returns access token in response body, refresh token set in HTTP Only cookie.
    """
    token: str


@dataclass(frozen=True)
class AuthErrors:
    INVALID_CREDENTIALS: str = "Invalid credentials"
    ACCOUNT_NOT_ACTIVE: str = "Account is not activated"
    INVALID_TOKEN: str = "Invalid token"
    TOKEN_EXPIRED: str = "Token has expired"


class SignInErrorSchema(Schema):
    """
    Authentication Error Responses:
    - 401:
        - Invalid credentials
        - Account not activated
    """
    error: str = Field(
        ...,
        description="Error message",
        example=AuthErrors.INVALID_CREDENTIALS
    )


class SignInSchema(Schema):
    email: str
    password: str
