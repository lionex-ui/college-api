from fastapi import APIRouter, Depends

from app.repositories import UsersRepository
from app.schemas import LoggedInResponse, UserNotFoundError, UsersSchema, WrongPasswordError

router = APIRouter(prefix="/users", tags=["Users management"])


@router.post(
    "",
    response_model=LoggedInResponse,
    responses={404: {"model": UserNotFoundError}, 401: {"model": WrongPasswordError}},
)
async def login(user: UsersSchema, users_repo: UsersRepository = Depends()):
    return await users_repo.login(user)
