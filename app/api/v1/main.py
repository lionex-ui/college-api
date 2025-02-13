from fastapi import APIRouter

from app.api.v1 import headers

router = APIRouter()

router.include_router(headers.router)
