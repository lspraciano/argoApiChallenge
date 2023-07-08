from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pytz import timezone

from configuration.configs import settings

oauth2_schema: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_URL}/users/authentication"
)


def _get_access_token(
        token_type: str,
        expire_time: timedelta,
        sub: str
) -> str:
    payload: dict = {}

    sp: timezone = timezone("America/Sao_Paulo")
    expire: datetime = datetime.now(tz=sp) + expire_time

    payload["type"]: str = token_type

    payload["exp"]: datetime = expire

    payload["iat"]: datetime = datetime.now(tz=sp)

    payload["sub"]: str = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def get_access_token(
        sub: str
) -> str:
    return _get_access_token(
        token_type='access_token',
        expire_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )