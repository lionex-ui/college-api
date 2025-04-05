from fastapi import APIRouter, Depends

from app.repositories import PagesRepository
from app.schemas import AddPageResponse, DeletePageResponse, PagesSchema, BlocksSchema

router = APIRouter(prefix="/pages", tags=["Pages management"])


@router.post("", response_model=AddPageResponse)
async def add_page(page: PagesSchema, pages_repo: PagesRepository = Depends()):
    await pages_repo.add(page)
    return AddPageResponse()


@router.get("", response_model=list[str])
async def get_page_urls(pages_repo: PagesRepository = Depends()):
    page_urls = await pages_repo.get()
    return page_urls


@router.get("/{page_url}", response_model=PagesSchema | None)
async def get_full_page_data(page_url: str, pages_repo: PagesRepository = Depends()):
    page = await pages_repo.get_full_page_date(page_url)
    if page is None:
        return None

    page_schema = PagesSchema(
        url=page.url,
        content=[
            BlocksSchema(block_id=block.block_id, content=block.content, type=block.type) for block in page.blocks
        ],
    )
    page_schema.content.sort(key=lambda block: int(block.block_id.strip(":r")))

    return page_schema


@router.delete("/{page_url}", response_model=DeletePageResponse)
async def delete_page(page_url: str, pages_repo: PagesRepository = Depends()):
    await pages_repo.delete(page_url)
    return DeletePageResponse()
