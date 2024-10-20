import asyncio

import httpx
from pydantic import BaseModel

from config import settings


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
    background_color: str | None = None
    supply: str | None = None


class OpenSea(BaseModel):
    collectionName: str
    collectionSlug: str
    safelistRequestStatus: str
    imageUrl: str
    description: str | None = None
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


async def get_nfts(owner_address) -> NFTData:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.RPC_URL}/getNFTs", params={"owner": owner_address})

        # Check if the request was successful
        if response.status_code == 200:
            nfts_data = response.json()
            return NFTData.model_validate(nfts_data)

        if response.status_code == 429:  # Too Many Requests
            await asyncio.sleep(5) # 5 sec
            response = await client.get(f"{settings.RPC_URL}/getNFTs", params={"owner": owner_address})
            # Check if the request was successful
            if response.status_code == 200:
                nfts_data = response.json()
                return NFTData.model_validate(nfts_data)

        raise RuntimeError("bad request from alchemy RPC_URL")
