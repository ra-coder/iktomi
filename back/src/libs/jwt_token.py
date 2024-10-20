import datetime

import jwt
from pydantic import BaseModel

from config import settings

TOKEN_EXPIRATION_HOURS = 1

class JWTPayload(BaseModel):
    user_id: int


def issue_jwt(user_data: JWTPayload) -> str:
    jwt_token = jwt.encode({
            'user': user_data.model_dump(),
            'iss': settings.ISSUER,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS)
        },
        settings.JWT_SECRET,
        algorithm='HS256',
    )
    return jwt_token


def validate_jwt(jwt_token: str) -> JWTPayload:
    # Decode JWT
    payload = jwt.decode(jwt_token, settings.JWT_SECRET, algorithms=['HS256'])

    # Validate the issuer (optional)
    if payload.get('iss') != settings.ISSUER:
        raise jwt.InvalidIssuerError("Invalid issuer")

    return JWTPayload.model_validate(payload)

