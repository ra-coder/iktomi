from fastapi import APIRouter

from api.web3.get_balance import balance_web3_router
from api.web3.get_contract_author import contract_info_web3_router
from api.web3.get_nft_list import web3_get_nfts_router

web3_router = APIRouter()
web3_router.include_router(balance_web3_router)
web3_router.include_router(contract_info_web3_router)
web3_router.include_router(web3_get_nfts_router)

__all_ = [
    "web3_router",
]
