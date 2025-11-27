from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.schemas.user import STR_NUMBER_FIELD, PHONE_NUMBER_FIELD


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    profession: str
    str_number: STR_NUMBER_FIELD
    medical_institutions: str
    phone_number: PHONE_NUMBER_FIELD = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
