from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

# Shared Field
STR_NUMBER_FIELD = Annotated[
    str, StringConstraints(pattern=r"\d", min_length=17, max_length=17)
]


PHONE_NUMBER_FIELD = Annotated[
    Optional[str],
    StringConstraints(pattern=r"^0[1-9][0-9]{7,14}$"),
]


# Route Schema
class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserCredentials):
    str_number: str
    profession: str
    str_number: STR_NUMBER_FIELD
    medical_institutions: str
    phone_number: PHONE_NUMBER_FIELD


class UserLogin(UserCredentials):
    pass


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
