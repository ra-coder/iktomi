import datetime

import jwt
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from config import settings

TOKEN_EXPIRATION_HOURS = 1
JWT_ALGORITHM = "HS256"


class JWTPayload(BaseModel):
    user_id: int


def issue_jwt(user_data: JWTPayload) -> str:
    jwt_token = jwt.encode({
        "user": user_data.model_dump(),
        "iss": settings.ISSUER,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS)
    },
        settings.JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return jwt_token


def validate_jwt(jwt_token: str) -> JWTPayload:
    # Decode JWT
    payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=[JWT_ALGORITHM])

    # Validate the issuer (optional)
    if payload.get('iss') != settings.ISSUER:
        raise jwt.InvalidIssuerError("Invalid issuer")

    return JWTPayload.model_validate(payload["user"])


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

    return payload.user_id
