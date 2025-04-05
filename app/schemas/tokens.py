from pydantic import Field

from app.schemas.config_base_model import Schema


class RefreshTokensRequest(Schema):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class RefreshTokenResponse(Schema):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class RefreshTokenExpiredError(Schema):
    message: str = "Refresh token has expired"


class AccessTokenNotExpired(Schema):
    message: str = "Access token has not expired"


class AccessTokenExpiredError(Schema):
    message: str = "Access token has expired"
