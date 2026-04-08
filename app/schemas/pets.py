
from datetime import datetime
from pydantic import Field
from .base import BaseRequest, BaseResponse


# Base
class PetBase(BaseRequest):
    pet_name: str = Field(..., min_length=1, max_length=50, description="Pet's name")


# Create
class PetCreate(PetBase):
    pass

class PetCreateAdmin(PetBase):
    owner_id: int = Field(..., description="ID of the pet's owner")


# Update
class PetUpdate(BaseRequest):
    pet_name: str | None = Field(default=None, min_length=1, max_length=50, description="Pet's name")


class PetUpdateAdmin(PetUpdate):
    owner_id: int | None = Field(default=None, description="ID of the pet's owner")


# Read
class PetRead(BaseResponse):
    id: int
    pet_name: str
    create_time: datetime
    update_time: datetime


class PetReadAdmin(PetRead):
    owner_id: int
    is_deleted: bool


class PetPageResponse(BaseResponse):
    items: list[PetRead]
    total: int
    page: int
    pages: int
    limit: int


class PetAdminPageResponse(BaseResponse):
    items: list[PetReadAdmin]
    total: int
    page: int
    pages: int
    limit: int


