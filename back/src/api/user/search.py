from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select

from db import User, Wallet
from db.connect import AsyncSessionLocal, get_async_db_session

users_search_router = APIRouter()


class WalletInfo(BaseModel):
    id: int
    address: str
    is_confirmed: bool


class UserInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    wallets: list[WalletInfo] | None


class UsersInfo(BaseModel):
    users: list[UserInfo] = []


@users_search_router.post("/api/users/search", response_model=UsersInfo)
async def users_search(
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> UsersInfo:
    query = select(
        func.jsonb_build_object(
            'id', User.id,
            'email', User.email,
            'first_name', User.first_name,
            'last_name', User.last_name,
            'wallets', func.array_agg(
                func.jsonb_build_object(
                    'id', Wallet.id,
                    'address', Wallet.address,
                    'is_confirmed', Wallet.is_confirmed,
                ),
            ).filter(Wallet.id.isnot(None)),
        ),
    ).select_from(
        User,
    ).outerjoin(
        Wallet,
        Wallet.user_id == User.id,
    ).group_by(
        User.id,
    ).order_by(
        User.last_name,
        User.first_name,
    )
    result = await async_db_session.execute(query)
    return UsersInfo(users=result.scalars())
