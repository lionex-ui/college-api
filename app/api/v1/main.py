from fastapi import APIRouter

from app.api.v1 import headers, pages

router = APIRouter()

router.include_router(headers.router)
router.include_router(pages.router)
