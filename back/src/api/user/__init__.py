from fastapi import APIRouter

from api.user.myself import user_myself_router
from api.user.nfts import user_nfts_router
from api.user.search import users_search_router

user_router = APIRouter()
user_router.include_router(user_nfts_router)
user_router.include_router(users_search_router)
user_router.include_router(user_myself_router)

__all_ = [
    "user_router",
]
