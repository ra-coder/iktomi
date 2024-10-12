from fastapi import APIRouter, Depends
from pydantic import BaseModel

from db.connect import get_db_session
from db.oauth import OAuthAccount

vk_login_router = APIRouter()

VK_PROVIDER_ID = 1


class VKTokens(BaseModel):
    refresh_token: str
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    user_id: int
    state: str
    scope: str


class SimpleResponse(BaseModel):
    success: bool


@vk_login_router.post("/api/vk/login/tokens")
def read_root(
    data: VKTokens,
    db_session: Depends(get_db_session)
) -> SimpleResponse:
    # TODO search for existing user if don't exists -> create new
    # TODO create user

    account = OAuthAccount(
        # user_id=1,
        provider_id=VK_PROVIDER_ID,
        provider_user_id=data.user_id,
        access_token=data.access_token,
        refresh_token=data.refresh_token,
    )
    db_session.add(account)
    db_session.commit()
    return SimpleResponse(success=True)
