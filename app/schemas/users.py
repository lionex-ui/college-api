from pydantic import Field

from app.schemas.config_base_model import Schema


class UsersSchema(Schema):
    username: str = Field(max_length=32)
    password: str


class LoggedInResponse(Schema):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class UserNotFoundError(Schema):
    message: str = "User not found"


class WrongPasswordError(Schema):
    message: str = "Wrong password"


class UserCreatedResponse(Schema):
    message: str = "User created successfully"


class UsernameAlreadyExistsError(Schema):
    message: str = "Username already exists"


class UserDeletedResponse(Schema):
    message: str = "User deleted successfully"


class NoPrivilegeError(Schema):
    message: str = "No privilege"
