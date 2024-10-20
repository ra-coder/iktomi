from typing import Any

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from config import settings

contract_info_web3_router = APIRouter()


async def get_contact_creator(contract_address: str) -> Any:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.RPC_URL}/getContractMetadata",
            params={"contractAddress": contract_address},
            headers={"accept": "application/json"}
        )

        # Check if the request was successful
        if response.status_code == 200:
            contact_meta_data = response.json()
            return contact_meta_data
        raise RuntimeError("bad request from alchemy RPC_URL")


class ContactRequest(BaseModel):
    address: str


@contract_info_web3_router.post("/api/web3/contract-info")
async def get_wallet_info(contract: ContactRequest):
    creator = await get_contact_creator(contract.address)
    return {"creator": creator}
