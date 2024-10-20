from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select

from db import User, Wallet
from db.connect import AsyncSessionLocal, get_async_db_session
from libs.jwt_token import get_user_id_from_token

user_myself_router = APIRouter()


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


@user_myself_router.get("/api/user/myself", response_model=UserInfo)
async def get_myself(
    token_user_id: int = Depends(get_user_id_from_token),
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> UserInfo:
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
    ).where(
        User.id == token_user_id
    ).group_by(
        User.id,
    )
    result = await async_db_session.execute(query)
    user_info_with_wallets = UserInfo(**result.scalar_one_or_none())

    return user_info_with_wallets
