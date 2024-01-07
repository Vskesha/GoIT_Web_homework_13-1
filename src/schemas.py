from datetime import datetime, date
from typing import Optional, Union

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(default=" ", examples=["Vasyl", "Katya"], min_length=1, max_length=25, title="first name")
    last_name: str = Field(default=" ", examples=["Ivanenko", "Kozak"], min_length=1, max_length=25, title="last name")
    email: EmailStr
    phone: Union[str, None] = Field(None, max_length=25, title="Phone number")
    birthday: Optional[date] = None
    comments: Union[str, None] = Field(default=None, title="Comments")
    favorite: bool = False


class ContactFavoriteModel(BaseModel):
    favorite: bool = False


class ContactResponse(BaseModel):
    id: int
    first_name: Union[str, None]
    last_name: Union[str, None]
    email: Union[EmailStr, None]
    phone: Union[str, None]
    birthday: Union[date, None]
    comments: Union[str, None]
    favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
