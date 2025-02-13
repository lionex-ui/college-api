from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.models.header_tabs import HeaderTabsModel
from app.models.headers import HeadersModel
from app.schemas.headers import HeadersSchema, HeaderTabsSchema


class HeadersRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def add(self, headers: list[HeadersSchema]) -> None:
        await self.session.execute(delete(HeadersModel))

        new_headers = []
        new_tabs = []

        for header in headers:
            new_headers.append(
                HeadersModel(
                    header_name=header.header_name,
                    header_url=str(header.header_url) if header.header_url else None,
                )
            )

        self.session.add_all(new_headers)
        await self.session.flush()

        for header, new_header in zip(headers, new_headers):
            for tab in header.tabs:
                new_tabs.append(
                    HeaderTabsModel(
                        header_id=new_header.id,
                        tab_name=tab.tab_name,
                        tab_url=str(tab.tab_url) if tab.tab_url else None,
                    )
                )

        self.session.add_all(new_tabs)
        await self.session.commit()

    async def get(self) -> list[HeadersSchema]:
        result = await self.session.execute(
            select(HeadersModel)
            .options(selectinload(HeadersModel.tabs))
            .order_by(HeadersModel.id)
        )
        headers = result.scalars().all()

        return [
            HeadersSchema(
                header_name=header.header_name,
                header_url=header.header_url,
                tabs=[
                    HeaderTabsSchema(tab_name=tab.tab_name, tab_url=tab.tab_url)
                    for tab in header.tabs
                ],
            )
            for header in headers
        ]
