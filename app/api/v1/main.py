from fastapi import APIRouter

from app.api.v1 import headers, pages, tokens, users

router = APIRouter()

router.include_router(headers.router)
router.include_router(pages.router)
router.include_router(users.router)
router.include_router(tokens.router)
