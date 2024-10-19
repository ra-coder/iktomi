from decimal import Decimal
from typing import Any

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from config import settings

web3_get_nfts_router = APIRouter()


class CurrencyValue(BaseModel):
    code: str
    value: Decimal


class WalletRequest(BaseModel):
    address: str


class WalletResponse(BaseModel):
    address: str
    data: Any


async def get_nfts(owner_address):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.RPC_URL}/getNFTs", params={"owner": owner_address})

        # Check if the request was successful
        if response.status_code == 200:
            nfts_data = response.json()
            return nfts_data
        raise RuntimeError("bad request from alchemy RPC_URL")


@web3_get_nfts_router.post("/api/web3/get_nft_list", response_model=WalletResponse)
async def get_nft_list(wallet: WalletRequest):
    return WalletResponse(
        address=wallet.address,
        data=await get_nfts(wallet.address)
    )
