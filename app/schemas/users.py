from pydantic import Field

from app.schemas.config_base_model import Schema


class UsersSchema(Schema):
    username: str = Field(max_length=32)
    password: str


class LoggedInResponse(Schema):
    message: str = "Successfully logged in"


class UserNotFoundError(Schema):
    message: str = "User not found"


class WrongPasswordError(Schema):
    message: str = "Wrong password"
