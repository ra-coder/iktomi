import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select

from db.connect import AsyncSessionLocal, get_async_db_session
from db.oauth import OAuthAccount, RawExternalData, OAuthProvider
from db.user import User

github_login_router = APIRouter()

GITHUB_PROVIDER_ID = 1
GITHUB_CLIENT_ID = "Ov23lin4GfC1NKNE4u6p"


class GithubCode(BaseModel):
    code: str


class UserInfo(BaseModel):
    id: int
    email: str
    name: str


@github_login_router.post("/api/github/login/tokens")
async def read_root(
    user_tokens_data: GithubCode,
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> UserInfo:
    """
      const response = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: client_id,
          client_secret: 'your_github_client_secret',  // Replace with your secret
          code: code,
          redirect_uri: redirect_uri
        })
      });

      const data = await response.text();
      const params = new URLSearchParams(data);
      res.json({ access_token: params.get('access_token') });

        // Fetch User Data (Step 4)
        async function fetchGitHubUser(token) {
          try {
            const response = await fetch('https://api.github.com/user', {
              headers: { Authorization: `token ${token}` }
            });
            return await response.json();
          } catch (error) {
            console.error('Error fetching user data:', error);
          }
        }
    """
    stmt = select(
        OAuthProvider.client_secret,
    ).select_from(
        OAuthProvider,
    ).where(
        OAuthProvider.id == GITHUB_PROVIDER_ID,
    )
    result = await async_db_session.execute(stmt)
    secret = result.scalar_one()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://github.com/login/oauth/access_token",
            headers={"Content-Type": "application/json"},
            json={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": secret,
                "code": GithubCode.code,
                "redirect_uri": "https://iktomi.pro/github-login",
            },
        )
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            raise RuntimeError(f"Error: {data}")
        return data
    else:
        raise RuntimeError("Bad github response")


    # result = await async_db_session.execute(
    #     select(
    #         User.id,
    #         User.email,
    #     ).select_from(
    #         User,
    #     ).join(
    #         OAuthAccount,
    #         OAuthAccount.user_id == User.id,
    #     ).where(
    #         OAuthAccount.provider_id == GITHUB_PROVIDER_ID,
    #         OAuthAccount.provider_user_id == str(user_tokens_data.user_id),
    #     )
    # )
    # row = result.scalar_one_or_none()
    # if row is not None:
    #     user_id, user_email = row
    #     return UserInfo(user_id=user_id, email=user_email)

    # github_user_info = await get_github_user_info(user_tokens_data.id_token)
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
