from fastapi import APIRouter, Depends

from app.repositories.headers import HeadersRepository
from app.schemas.headers import HeadersResponse, HeadersSchema

router = APIRouter(prefix="/headers", tags=["Headers management"])


@router.post("/", response_model=HeadersResponse)
async def add_headers(
    headers: list[HeadersSchema], headers_repo: HeadersRepository = Depends()
):
    await headers_repo.add(headers)
    return HeadersResponse()


@router.get("/", response_model=list[HeadersSchema])
async def get_headers(headers_repo: HeadersRepository = Depends()):
    return await headers_repo.get()
