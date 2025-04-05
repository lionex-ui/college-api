from fastapi import Depends
from sqlalchemy import exc as sql_exc
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models import UsersModel
from app.schemas import UsersSchema


class UsersRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def login(self, user: UsersSchema) -> tuple[int, str | None, bool | None]:
        result = await self.session.execute(select(UsersModel).filter(UsersModel.username == user.username))
        user_from_db = result.scalar()

        if user_from_db is None:
            return 404, None, None

        if user_from_db.password != user.password:
            return 401, None, None

        return 200, user_from_db.username, user_from_db.is_main_administrator

    async def create_user(self, user: UsersSchema) -> int:
        new_user = UsersModel(username=user.username, password=user.password)
        self.session.add(new_user)

        try:
            await self.session.commit()
            return 200
        except sql_exc.IntegrityError:
            await self.session.rollback()
            return 409

    async def delete_user(self, username: str) -> None:
        await self.session.execute(delete(UsersModel).filter(UsersModel.username == username))
        await self.session.commit()
