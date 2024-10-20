from fastapi import APIRouter, Depends
from pydantic import BaseModel

from db import Wallet
from db.connect import AsyncSessionLocal, get_async_db_session
from libs.jwt_token import get_user_id_from_token

add_user_wallet_router = APIRouter()


class WalletAddress(BaseModel):
    address: str


class WalletInfo(BaseModel):
    id: int
    address: str
    is_confirmed: bool


@add_user_wallet_router.post("/api/user/add_wallet", response_model=WalletInfo)
async def get_myself(
    payload: WalletAddress,
    token_user_id: int = Depends(get_user_id_from_token),
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> WalletInfo:
    wallet = Wallet(
        user_id=token_user_id,
        address=payload.address,
    )
    async_db_session.add(wallet)
    await async_db_session.commit()
    return WalletInfo(
        id=wallet.id,
        address=wallet.address,
        is_confirmed=wallet.is_confirmed,
    )
