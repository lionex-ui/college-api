from fastapi import APIRouter, Depends, HTTPException, Request

from app.repositories import UsersRepository
from app.schemas import (
    LoggedInResponse,
    NoPrivilegeError,
    UserCreatedResponse,
    UsernameAlreadyExistsError,
    UserNotFoundError,
    UsersSchema,
    WrongPasswordError,
    UserDeletedResponse,
)
from app.utils import JWT

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=LoggedInResponse,
    responses={404: {"model": UserNotFoundError}, 401: {"model": WrongPasswordError}},
)
async def login(
    user: UsersSchema = Depends(UsersSchema), users_repo: UsersRepository = Depends(), jwt_system: JWT = Depends()
):
    status_code, username, is_main_administrator = await users_repo.login(user)

    if status_code == 200:
        access_token, refresh_token, refresh_string = jwt_system.generate_token(username, is_main_administrator)
        return LoggedInResponse(access_token=access_token, refresh_token=refresh_token)
    elif status_code == 404:
        raise HTTPException(status_code=status_code, detail=UserNotFoundError().model_dump())
    elif status_code == 401:
        raise HTTPException(status_code=status_code, detail=WrongPasswordError().model_dump())


@router.post(
    "",
    response_model=UserCreatedResponse,
    responses={409: {"model": UsernameAlreadyExistsError}, 401: {"model": NoPrivilegeError}},
)
async def create_user(
    request: Request, user: UsersSchema, users_repo: UsersRepository = Depends()
):
    if not request.state.payload["is_main_administrator"]:
        raise HTTPException(status_code=401, detail=NoPrivilegeError().model_dump())

    status_code = await users_repo.create_user(user)
    if status_code == 200:
        return UserCreatedResponse()
    elif status_code == 409:
        raise HTTPException(status_code=status_code, detail=UsernameAlreadyExistsError().model_dump())


@router.delete("/{username}", response_model=UserDeletedResponse, responses={401: {"model": NoPrivilegeError}})
async def delete_user(request: Request, username: str, users_repo: UsersRepository = Depends()):
    if not request.state.payload["is_main_administrator"]:
        raise HTTPException(status_code=401, detail=NoPrivilegeError().model_dump())

    await users_repo.delete_user(username)
    return UserDeletedResponse()
