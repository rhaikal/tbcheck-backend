from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
