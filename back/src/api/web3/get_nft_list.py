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

class Contract(BaseModel):
    address: str


class TokenMetadata(BaseModel):
    tokenType: str


class Id(BaseModel):
    tokenId: str
    tokenMetadata: TokenMetadata


class TokenUri(BaseModel):
    gateway: str
    raw: str


class MediaItem(BaseModel):
    gateway: str
    thumbnail: str
    raw: str
    format: str
    bytes: int


class Metadata(BaseModel):
    name: str
    description: str
    image: str
    external_url: str
    background_color: str
    supply: str


class OpenSea(BaseModel):
    collectionName: str
    collectionSlug: str
    safelistRequestStatus: str
    imageUrl: str
    description: str
    lastIngestedAt: str


class ContractMetadata(BaseModel):
    name: str
    symbol: str
    tokenType: str
    openSea: OpenSea


class OwnedNft(BaseModel):
    contract: Contract
    id: Id
    balance: str
    title: str
    description: str
    tokenUri: TokenUri
    media: list[MediaItem]
    metadata: Metadata
    timeLastUpdated: str
    contractMetadata: ContractMetadata


class NFTData(BaseModel):
    ownedNfts: list[OwnedNft]
    totalCount: int
    blockHash: str


class WalletRequest(BaseModel):
    address: str


class WalletResponse(BaseModel):
    address: str
    data: NFTData


async def get_nfts(owner_address) -> NFTData:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.RPC_URL}/getNFTs", params={"owner": owner_address})

        # Check if the request was successful
        if response.status_code == 200:
            nfts_data = response.json()
            return NFTData.model_validate(nfts_data)
        raise RuntimeError("bad request from alchemy RPC_URL")


@web3_get_nfts_router.post("/api/web3/get_nft_list", response_model=WalletResponse)
async def get_nft_list(wallet: WalletRequest):
    return WalletResponse(
        address=wallet.address,
        data=await get_nfts(wallet.address)
    )
