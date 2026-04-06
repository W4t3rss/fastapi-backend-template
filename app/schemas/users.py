
from datetime import datetime
from pydantic import Field, field_validator
from .base import BaseRequest, BaseResponse
from .validator import validate_phone_number 


# Base
class UserBase(BaseRequest):
    user_name: str = Field(..., min_length=2, max_length=50, description="User's name")
    phone_number: str = Field(..., max_length=20, description="User's phone number")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        return validate_phone_number(value)


# Create
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255, description="User's password") 


class UserCreateAdmin(UserCreate):
    role: int = Field(default=0, description="User's role, 0 for regular user, 1 for admin")


# Update
class UserUpdate(BaseRequest):
    user_name: str | None = Field(default=None, min_length=2, max_length=50, description="User's name")
    phone_number: str | None = Field(default=None, max_length=20, description="User's phone number")
    password: str | None = Field(default=None, min_length=6, max_length=255, description="User's password")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        return validate_phone_number(value)

class UserUpdateAdmin(UserUpdate):
    role: int | None = Field(default=None, description="User's role, 0 for regular user, 1 for admin")


# Read
class UserRead(BaseResponse):
    id: int
    user_name: str
    phone_number: str | None
    create_time: datetime
    update_time: datetime


class UserReadAdmin(UserRead):
    role: int
    is_deleted: bool
    code: str | None
    code_expire_time: datetime | None