from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import and_, delete

from db import Wallet
from db.connect import AsyncSessionLocal, get_async_db_session
from libs.jwt_token import get_user_id_from_token

delete_user_wallet_router = APIRouter()


class WalletInfo(BaseModel):
    id: int


@delete_user_wallet_router.post("/api/user/delete_wallet")
async def get_myself(
    payload: WalletInfo,
    token_user_id: int = Depends(get_user_id_from_token),
    async_db_session: AsyncSessionLocal = Depends(get_async_db_session),
) -> None:
    query = delete(
        Wallet,
    ).where(
        and_(
            Wallet.user_id == token_user_id,
            Wallet.id == payload.id,
        )
    )
    await async_db_session.execute(query)
    await async_db_session.commit()
