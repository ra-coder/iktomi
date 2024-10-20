import httpx
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import and_, select

from config import settings
from db.connect import AsyncSessionLocal, get_async_db_session
from db.oauth import OAuthAccount, RawExternalData
from db.user import User
from libs.jwt_token import JWTPayload, issue_jwt

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


class UserInfo(BaseModel):
    id: int
    email: str | None = None
    name: str | None = None


@vk_login_router.post("/api/vk/login/tokens", response_model=UserInfo)
async def read_root(
    user_tokens_data: VKTokens,
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> JSONResponse:
    user = await get_or_create_user(user_tokens_data, async_db_session)

    jwt_token = issue_jwt(JWTPayload(user_id=user.id))

    response = JSONResponse(content=UserInfo(id=user.id, email=user.email, name=user.first_name))
    response.set_cookie(key='jwt_token', value=jwt_token, httponly=True, secure=True, domain=settings.DOMAIN)

    return response


async def get_or_create_user(
    vk_tokens_data: VKTokens,
    async_db_session: AsyncSessionLocal,
) -> UserInfo:
    result = await async_db_session.execute(
        select(
            User.id,
            User.email,
            User.first_name,
        ).select_from(
            User,
        ).join(
            OAuthAccount,
            OAuthAccount.user_id == User.id,
        ).where(
            and_(
                OAuthAccount.provider_id == settings.VK_PROVIDER_ID,
                OAuthAccount.provider_user_id == str(vk_tokens_data.user_id),
            ),
        )
    )
    user_row = result.one_or_none()
    if user_row is None:
        user = await create_vk_user(vk_tokens_data, async_db_session)
    else:
        user_id, user_email, user_first_name = user_row
        user = UserInfo(id=user_id, email=user_email, name=user_first_name)
    return user


async def create_vk_user(
    vk_tokens_data: VKTokens,
    async_db_session: AsyncSessionLocal,
) -> UserInfo:
    vk_user_info = await get_vk_user_info(vk_tokens_data.id_token)
    user = User(
        email=vk_user_info.get("email"),
        first_name=vk_user_info.get("first_name"),
        last_name=vk_user_info.get("last_name"),
    )
    async_db_session.add(user)
    await async_db_session.flush()
    account = OAuthAccount(
        user_id=user.id,
        provider_id=settings.VK_PROVIDER_ID,
        provider_user_id=str(vk_tokens_data.user_id),
        access_token=vk_tokens_data.access_token,
        refresh_token=vk_tokens_data.refresh_token,
        token_id=vk_tokens_data.id_token,
    )
    async_db_session.add(account)
    row_data = RawExternalData(
        user_id=user.id,
        provider_id=settings.VK_PROVIDER_ID,
        provider_user_id=str(vk_tokens_data.user_id),
        data=vk_user_info,
    )
    async_db_session.add(row_data)
    await async_db_session.commit()
    return UserInfo(id=user.id, email=user.email, name=user.first_name)


async def get_vk_user_info(user_access_token: str):
    """
        POST https://id.vk.com/oauth2/public_info

        Content-Type: application/x-www-form-urlencoded

        client_id=<идентификатор приложения>
        & id_token=<JSON Web Token пользователя>
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://id.vk.com/oauth2/public_info",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            content=f"client_id={settings.VK_CLIENT_ID}&id_token={user_access_token}",
        )
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            raise RuntimeError(f"Error: {data}")
        return data["user"]
    raise RuntimeError("Bad vk response")
