from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import User
from app.schemas.user import UserRegister
from config import settings


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def user_exists(email: str, session: AsyncSession) -> bool:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first() is not None


async def register_user(
    user_data: UserRegister,
    session: AsyncSession,
) -> User:
    new_user = User(
        email=user_data.email,
        password=get_password_hash(user_data.password),
        profession=user_data.profession,
        str_number=user_data.str_number,
        medical_institutions=user_data.medical_institutions,
        phone_number=user_data.phone_number,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


def validate_invitation_code(code: str) -> bool:
    return code == settings.invitation_code


def authenticate_user(user: User, password: str) -> bool:
    return verify_password(password, user.password)


def create_token_response(user_id: int) -> dict:
    access_token = create_access_token({"sub": str(user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
