from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_session
from app.core.security import decode_access_token, oauth2_scheme
from app.models import User

UNAUTHORIZED_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "type": "unauthorized",
        "loc": ["headers", "authorization"],
        "msg": "Invalid token",
        "input": None,
        "ctx": {},
    },
)

USER_NOT_FOUND_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "type": "user_not_found",
        "loc": ["body", "user_id"],
        "msg": "User not found",
        "input": None,
        "ctx": {},
    },
)


async def require_auth(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise UNAUTHORIZED_ERROR

    user_id = payload.get("sub")
    if not user_id:
        raise UNAUTHORIZED_ERROR

    result = await session.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()

    if not user:
        raise USER_NOT_FOUND_ERROR

    return user
