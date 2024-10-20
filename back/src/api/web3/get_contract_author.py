import asyncio
from typing import Any

from eth_typing import Address, HexStr
from fastapi import APIRouter
from pydantic import BaseModel
from web3 import Web3

from config import settings

contract_info_web3_router = APIRouter()


def get_contact_creator(contract_address: str) -> str | Any:
    w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))

    # contract_address = Address(bytes.fromhex(contract_address[2:]))  # address str without 0x prefix
    contract_address = HexStr(contract_address[2:])
    transaction = w3.eth.get_transaction_receipt(contract_address)
    # transaction = w3.eth.get_transaction_by_block(contract_address, 0)
    # creator_address = transaction['from']
    # return creator_address
    return transaction


async def get_contact_creator_async(contract_address: str):
    return await asyncio.to_thread(get_contact_creator, (contract_address))


class ContactRequest(BaseModel):
    address: str


@contract_info_web3_router.post("/api/web3/contract-info")
async def get_wallet_info(contract: ContactRequest):
    creator = await get_contact_creator_async(contract.address)
    return {"creator": creator}
