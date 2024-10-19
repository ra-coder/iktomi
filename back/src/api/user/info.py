from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select

from db import User, Wallet
from db.connect import AsyncSessionLocal, get_async_db_session
from integrations.poligon import NFTData, get_nfts

users_info_router = APIRouter()


class WalletInfo(BaseModel):
    id: int
    address: str
    is_confirmed: bool
    nfts: NFTData | None = None


class UserInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    wallets: list[WalletInfo] | None


@users_info_router.get("/api/user/{user_id: int}", response_model=UserInfo)
async def users_info(
    user_id: int,
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
        User.id == user_id,
    ).group_by(
        User.id,
    )
    result = await async_db_session.execute(query)
    info = result.scalar_one_or_none()
    if info is None:
        raise HTTPException(status_code=404, detail="user not found")
    info = UserInfo.model_validate(info)
    if info.wallets is None:
        info.wallets = []
    for wallet in info.wallets:
        wallet.nfts = await get_nfts(wallet.address)
    return info
