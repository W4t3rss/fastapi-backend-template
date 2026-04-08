
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps.get_db import get_db
from app.core.security.jwt import verify_access_token
from app.crud.users import get_user_by_id
from app.exceptions.auth import TokenExpiredException, TokenInvalidException
from app.exceptions.users import UserNotFoundException
from app.models.users import Users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Users:
    try:
        sub = verify_access_token(token)
    except ExpiredSignatureError as e:
        raise TokenExpiredException() from e
    except JWTError as e:
        raise TokenInvalidException(details=str(e)) from e
    
    try:
        user_id = int(sub)
    except (TypeError, ValueError) as e:
        raise TokenInvalidException(details="Invalid token subject") from e

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundException()

    return user