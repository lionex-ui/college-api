from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.models import BlocksModel, PagesModel
from app.schemas import BlocksSchema, PagesSchema


class PagesRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def add(self, page: PagesSchema) -> None:
        await self.session.execute(delete(PagesModel).filter(PagesModel.url == page.url))

        new_page = PagesModel(url=page.url)
        new_blocks = [
            BlocksModel(page_url=page.url, block_id=block.block_id, content=block.content, type=block.type)
            for block in page.content
        ]

        self.session.add(new_page)
        self.session.add_all(new_blocks)

        await self.session.commit()

    async def get(self) -> list[str]:
        result = await self.session.execute(select(PagesModel.url))
        page_urls = list(result.scalars().all())

        return page_urls

    async def get_full_page_date(self, page_url: str) -> PagesModel | None:
        result = await self.session.execute(
            select(PagesModel).options(selectinload(PagesModel.blocks)).filter(PagesModel.url == page_url)
        )
        page = result.scalar()

        return page

    async def delete(self, page_url: str) -> None:
        await self.session.execute(delete(PagesModel).filter(PagesModel.url == page_url))
        await self.session.commit()
