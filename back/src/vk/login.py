from fastapi import APIRouter
from pydantic import BaseModel

vk_login_router = APIRouter()


class VKTokens(BaseModel):
    refresh_token: str
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    user_id: int
    state: str
    scope: str


@vk_login_router.post("/api/vk/login/tokens")
def read_root(
    _data: VKTokens,
):
    raise NotImplementedError("TODO need store tokens to DB")
