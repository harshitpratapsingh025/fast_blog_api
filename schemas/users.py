import fastapi
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .admin.country_schema import CountrySchema
from .admin.language_schema import LanguageSchema


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserProfileBase(BaseModel):
    education: str | None = None
    addess: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    image: str | None = None
    language_id: int
    country_id: int
    user_id: int


class CreateUserProfile(UserProfileBase):
    pass


class UpdateUserProfile(UserProfileBase):
    id: int


class UserProfileSchema(UserProfileBase):
    id: int
    language: LanguageSchema = None
    user: UserSchema = None
    country: CountrySchema = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
