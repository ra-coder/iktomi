from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select

from db.connect import AsyncSessionLocal, get_async_db_session
from db.user import User

users_search_router = APIRouter()


class UserInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class UsersInfo(BaseModel):
    users: list[UserInfo] = []


@users_search_router.post("/api/users/search", response_model=UsersInfo)
async def users_search(
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> UsersInfo:
    query = select(
        func.array_agg(
            func.jsonb_build_object(
                'id', User.id,
                'email', User.email,
                'first_name', User.first_name,
                'last_name', User.last_name,
            ).order_by(
                User.last_name,
                User.first_name,
            ),
        )
    ).select_from(
        User,
    )
    result = await async_db_session.execute(query)
    return UsersInfo(users=result.scalar_one())
