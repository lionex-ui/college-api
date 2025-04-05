import re

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils import JWT


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.no_auth_paths = set()
        self.jwt_system = JWT()

        default_paths = ["GET /docs", "GET /redoc", "GET /openapi.json"]
        additional_paths = ["GET /headers", "GET /pages/[^/]+", "POST /tokens", "GET /users"]
        paths = default_paths + additional_paths

        self.add_paths(paths)

    def add_paths(self, paths: list[str]):
        for path in paths:
            self.no_auth_paths.add(path)

    async def dispatch(self, request: Request, call_next):
        path = f"{request.method} {request.url.path}"

        if not any(re.fullmatch(pattern, path) for pattern in self.no_auth_paths):
            auth_header = request.headers.get("Authorization")
            if not auth_header or "Bearer " not in auth_header:
                return JSONResponse(status_code=403, content={"detail": "Not authenticated"})

            token = auth_header.replace("Bearer ", "").strip()
            status_code, payload = self.jwt_system.verify_token(token)

            if status_code == 401:
                return JSONResponse(status_code=403, content={"detail": "Not authenticated"})

            request.state.payload = payload
        else:
            request.state.payload = None

        return await call_next(request)
