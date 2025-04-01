from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models import UsersModel
from app.schemas import LoggedInResponse, UserNotFoundError, UsersSchema, WrongPasswordError


class UsersRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def login(self, user: UsersSchema) -> LoggedInResponse:
        result = await self.session.execute(select(UsersModel).filter(UsersModel.username == user.username))
        user_from_db = result.scalar()

        if user_from_db is None:
            raise HTTPException(status_code=404, detail=UserNotFoundError().model_dump())

        if user_from_db.password != user.password:
            raise HTTPException(status_code=401, detail=WrongPasswordError().model_dump())

        return LoggedInResponse()
