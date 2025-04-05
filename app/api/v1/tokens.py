from fastapi import APIRouter, Depends, HTTPException

from app.schemas import AccessTokenNotExpired, RefreshTokenExpiredError, RefreshTokenResponse, RefreshTokensRequest
from app.utils import JWT

router = APIRouter(prefix="/tokens", tags=["JWT tokens"])


@router.post(
    "",
    response_model=RefreshTokenResponse,
    responses={401: {"model": RefreshTokenExpiredError}, 400: {"model": AccessTokenNotExpired}},
)
async def refresh_tokens(tokens: RefreshTokensRequest, jwt_system: JWT = Depends()):
    status_code, access_token, refresh_token, refresh_string = jwt_system.refresh_tokens(tokens)

    if status_code == 200:
        return RefreshTokenResponse(access_token=access_token, refresh_token=refresh_token)
    elif status_code == 401:
        raise HTTPException(status_code=status_code, detail=RefreshTokenExpiredError().model_dump())
    elif status_code == 400:
        raise HTTPException(status_code=status_code, detail=AccessTokenNotExpired().model_dump())
