from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.auth import (
    authenticate_user,
    create_token_response,
    get_user_by_email,
    register_user,
    user_exists,
    validate_invitation_code,
)
from app.schemas.user import UserRegister

router = APIRouter()

INVALID_INVITATION_CODE_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail={
        "type": "invalid_invitation_code",
        "loc": ["params", "invitation_code"],
        "msg": "Invalid invitation code",
        "input": None,
        "ctx": {},
    },
)

EMAIL_ALREADY_REGISTERED_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "type": "email_already_registered",
        "loc": ["body", "email"],
        "msg": "Email already registered",
        "input": None,
        "ctx": {},
    },
)

INVALID_CREDENTIALS_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "type": "invalid_credentials",
        "loc": ["body", "username", "password"],
        "msg": "Incorrect username or password",
        "input": None,
        "ctx": {},
    },
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/register")
async def register(
    user_data: UserRegister,
    invitation_code: str,
    session: AsyncSession = Depends(get_session),
):
    if not validate_invitation_code(invitation_code):
        raise INVALID_INVITATION_CODE_ERROR

    if await user_exists(user_data.email, session):
        raise EMAIL_ALREADY_REGISTERED_ERROR

    new_user = await register_user(user_data, session)
    return create_token_response(new_user.id)


@router.post("/login")
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_email(form_data.username, session)

    if not user or not authenticate_user(user, form_data.password):
        raise INVALID_CREDENTIALS_ERROR

    return create_token_response(user.id)
