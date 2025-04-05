from fastapi import APIRouter, Depends

from app.repositories import HeadersRepository
from app.schemas import HeadersResponse, HeadersSchema, HeaderTabsSchema

router = APIRouter(prefix="/headers", tags=["Headers management"])


@router.post("", response_model=HeadersResponse)
async def add_headers(headers: list[HeadersSchema], headers_repo: HeadersRepository = Depends()):
    await headers_repo.add(headers)
    return HeadersResponse()


@router.get("", response_model=list[HeadersSchema])
async def get_headers(headers_repo: HeadersRepository = Depends()):
    headers = await headers_repo.get()

    return [
        HeadersSchema(
            header_name=header.header_name,
            header_url=header.header_url,
            tabs=[HeaderTabsSchema(tab_name=tab.tab_name, tab_url=tab.tab_url) for tab in header.tabs],
        )
        for header in headers
    ]
