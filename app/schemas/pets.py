
from datetime import datetime
from pydantic import Field
from .base import BaseRequest, BaseResponse


# Base
class PetBase(BaseRequest):
    pet_name: str = Field(..., min_length=1, max_length=50, description="Pet name")


# Create
class PetCreate(PetBase):
    pass

class PetCreateAdmin(PetBase):
    owner_id: int = Field(..., description="Pet owner's ID")


# Update
class PetUpdate(BaseRequest):
    pet_name: str | None = Field(default=None, min_length=1, max_length=50, description="Pet name")


class PetUpdateAdmin(PetUpdate):
    owner_id: int | None = Field(default=None, description="Pet owner's ID")


# Read
class PetRead(BaseResponse):
    id: int
    pet_name: str
    create_time: datetime
    update_time: datetime


class PetReadAdmin(PetRead):
    owner_id: int
    is_deleted: bool


