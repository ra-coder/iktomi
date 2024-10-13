import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select

from db.connect import AsyncSessionLocal, get_async_db_session
from db.oauth import OAuthAccount, RawExternalData
from db.user import User

github_login_router = APIRouter()

GITHUB_PROVIDER_ID = 1
GITHUB_CLIENT_ID = "Ov23lin4GfC1NKNE4u6p"


class GithubTokens(BaseModel):
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
    email: str
    name: str


@github_login_router.post("/api/github/login/tokens")
async def read_root(
    user_tokens_data: GithubTokens,
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> UserInfo:
    result = await async_db_session.execute(
        select(
            User.id,
            User.email,
        ).select_from(
            User,
        ).join(
            OAuthAccount,
            OAuthAccount.user_id == User.id,
        ).where(
            OAuthAccount.provider_id == GITHUB_PROVIDER_ID,
            OAuthAccount.provider_user_id == str(user_tokens_data.user_id),
        )
    )
    row = result.scalar_one_or_none()
    if row is not None:
        user_id, user_email = row
        return UserInfo(user_id=user_id, email=user_email)

    github_user_info = await get_github_user_info(user_tokens_data.id_token)
    # user = User(
    #     email=vk_user_info.get("email"),
    #     first_name=vk_user_info.get("first_name"),
    #     last_name=vk_user_info.get("last_name"),
    # )
    # async_db_session.add(user)
    # await async_db_session.flush()
    # account = OAuthAccount(
    #     user_id=user.id,
    #     provider_id=GITHUB_PROVIDER_ID,
    #     provider_user_id=str(user_tokens_data.user_id),
    #     access_token=user_tokens_data.access_token,
    #     refresh_token=user_tokens_data.refresh_token,
    #     token_id=user_tokens_data.id_token,
    # )
    # async_db_session.add(account)
    # row_data = RawExternalData(
    #     user_id=user.id,
    #     provider_id=GITHUB_PROVIDER_ID,
    #     provider_user_id=str(user_tokens_data.user_id),
    #     data=vk_user_info,
    # )
    # async_db_session.add(row_data)
    # await async_db_session.commit()
    #
    # return UserInfo(id=user.id, email=user.email, name=user.first_name)


async def get_github_user_info(user_access_token: str):
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
            content=f"client_id={VK_CLIENT_ID}&id_token={user_access_token}",
        )
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            raise RuntimeError(f"Error: {data}")
        return data["user"]
    raise RuntimeError("Bad vk response")
