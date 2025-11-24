from pydantic import BaseModel, ConfigDict, EmailStr


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserCredentials):
    pass


class UserLogin(UserCredentials):
    pass


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
