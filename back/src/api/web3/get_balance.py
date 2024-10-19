import asyncio
from decimal import Decimal

from eth_typing import Address
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from web3 import Web3

from config import settings

web3_router = APIRouter()


# Contract ABI for ERC-721 (NFT standard), minimum required to interact with NFTs
# ERC721_ABI = '[{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{
# "name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}]'
# # Example function to fetch NFTs, here using an external API like Moralis (you can implement your own logic)
# async def fetch_nfts(wallet_address):
#     # Replace with your actual API for retrieving NFTs
#     # Example Moralis API request (you need an API key)
#     url = f"https://deep-index.moralis.io/api/v2/{wallet_address}/nft"
#     headers = {
#         "accept": "application/json",
#     }
#
#
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         if response.status_code != 200:
#             raise HTTPException(status_code=500, detail="Error fetching NFTs")
#         return response.json()


# Helper function to get Ether balance
def get_eth_balance(address: str):
    address = Address(bytes.fromhex(address))
    web3_api = Web3(Web3.HTTPProvider(settings.RPC_URL))

    if not web3_api.is_address(address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    balance_wei = web3_api.eth.get_balance(address)
    return web3_api.from_wei(balance_wei, unit='ether')


async def get_eth_balance_async(address: str):
    # Wrap the synchronous web3.eth.get_balance call in asyncio
    return await asyncio.to_thread(get_eth_balance, address)


class CurrencyValue(BaseModel):
    code: str
    value: Decimal


class WalletRequest(BaseModel):
    wallet_address: str
    balance: list[CurrencyValue]


class WalletInfo(BaseModel):
    wallet_address: str


@web3_router.post("/api/web3/wallet-info")
async def get_wallet_info(wallet: WalletRequest):
    # Get wallet balance
    balance = get_eth_balance(wallet.wallet_address)

    # Fetch NFTs
    # nfts = fetch_nfts(wallet.wallet_address)

    return WalletInfo(
        address=wallet.wallet_address,
        balance=[CurrencyValue(code="ETH", value=Decimal(balance))],
        # "nfts": nfts
    )
