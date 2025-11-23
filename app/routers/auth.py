from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_session
from app.core.security import create_access_token, get_password_hash, verify_password
from config import settings
from app.models import User
from app.schemas.user import UserRegister, UserLogin

router = APIRouter()


@router.post("/register")
async def register(
    user_data: UserRegister,
    invitation_code: str,
    session: AsyncSession = Depends(get_session),
):
    if invitation_code != settings.invitation_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid invitation code"
        )

    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    access_token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
