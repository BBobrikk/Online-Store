from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    firstname: str
    lastname: str


class UsersCreate(BaseUser):
    email: EmailStr
    password: str
    repeat_pass: str


class UsersRead(BaseUser):
    user_id: int
    email: EmailStr


class UsersUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None


class UsersCreds(BaseModel):
    email: EmailStr
    password: str
