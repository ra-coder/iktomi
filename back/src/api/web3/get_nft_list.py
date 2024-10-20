from fastapi import APIRouter
from pydantic import BaseModel

from integrations.poligon import NFTData, get_nfts

web3_get_nfts_router = APIRouter()


class WalletRequest(BaseModel):
    address: str


class WalletResponse(BaseModel):
    address: str
    data: NFTData


@web3_get_nfts_router.post("/api/web3/get_nft_list", response_model=WalletResponse)
async def get_nft_list(wallet: WalletRequest):
    return WalletResponse(
        address=wallet.address,
        data=await get_nfts(wallet.address)
    )
