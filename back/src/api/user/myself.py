import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response

from libs.jwt_token import JWTPayload, validate_jwt

user_myself_router = APIRouter()


def get_user_id_from_token(request: Request, response: Response) -> int:
    jwt_token = request.cookies.get('jwt_token')

    if not jwt_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = validate_jwt(jwt_token)
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidIssuerError,
        jwt.ExpiredSignatureError,
        jwt.InvalidTokenError,
    ) as err:
        response.delete_cookie("jwt_token")
        raise HTTPException(status_code=403, detail=f"invalid Token {err}")

    # user_info = users_db.get(payload.user_id)

    return payload.user_id


@user_myself_router.get("/api/user/myself")
async def get_myself(
    token_user_id: JWTPayload = Depends(get_user_id_from_token)
):
    return {"user_id": token_user_id}
