from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from app.core.security.jwt_token_manager import oauth2_schema
from configuration.configs import settings


async def get_user_id_from_token(
        token: str = Depends(oauth2_schema)
) -> str:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not authenticate user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: jwt.decode = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        user_id_from_token: str = payload.get("sub")
        if user_id_from_token is None:
            raise credential_exception

        return user_id_from_token

    except JWTError:
        raise credential_exception
