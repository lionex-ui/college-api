from fastapi import APIRouter, Depends

from app.repositories import PagesRepository
from app.schemas import AddPageResponse, DeletePageResponse, PagesSchema

router = APIRouter(prefix="/pages", tags=["Pages management"])


@router.post("", response_model=AddPageResponse)
async def add_page(page: PagesSchema, pages_repo: PagesRepository = Depends()):
    await pages_repo.add(page)
    return AddPageResponse()


@router.get("", response_model=list[str])
async def get_page_urls(pages_repo: PagesRepository = Depends()):
    return await pages_repo.get()


@router.get("/{page_url}", response_model=PagesSchema)
async def get_full_page_data(page_url: str, pages_repo: PagesRepository = Depends()):
    return await pages_repo.get_full_page_date(page_url)


@router.delete("/{page_url}", response_model=DeletePageResponse)
async def delete_page(page_url: str, pages_repo: PagesRepository = Depends()):
    await pages_repo.delete(page_url)
    return DeletePageResponse()
