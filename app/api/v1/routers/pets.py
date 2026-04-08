
from typing import Annotated
from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_current_user_pet, get_db
from app.models.pets import Pets
from app.models.users import Users
from app.schemas.pets import PetCreate, PetPageResponse, PetRead, PetUpdate
from app.services.pets import (
    create_pet_service,
    delete_pet_service,
    get_pets_by_owner_id_service,
    update_pet_service,
)
pets_router = APIRouter()


# app/api/v1/pets
@pets_router.post(
    "",
    response_model=PetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a pet for the current user",
)
async def create_pet(
    pet_create: PetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> PetRead:
    pet = await create_pet_service(db, current_user.id, pet_create)
    return PetRead.model_validate(pet)


# app/api/v1/pets
@pets_router.get(
    "",
    response_model=PetPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the current user's pet list",
)
async def get_my_pets(
    skip: int = Query(default=0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> PetPageResponse:
    result = await get_pets_by_owner_id_service(db, current_user.id, skip)
    return PetPageResponse.model_validate(result)


# app/api/v1/pets/{pet_id}
@pets_router.get(
    "/{pet_id}",
    response_model=PetRead,
    status_code=status.HTTP_200_OK,
    summary="Get a single pet for the current user",
)
async def get_pet(
    pet: Pets = Depends(get_current_user_pet),
) -> PetRead:
    return PetRead.model_validate(pet)


# app/api/v1/pets/{pet_id}
@pets_router.patch(
    "/{pet_id}",
    response_model=PetRead,
    status_code=status.HTTP_200_OK,
    summary="Update a pet for the current user",
)
async def update_pet(
    pet_id: int,
    pet_update: Annotated[
        PetUpdate,
        Body(
            openapi_examples={
                "rename_pet": {
                    "summary": "Rename the pet",
                    "value": {
                        "pet_name": "Buddy Jr.",
                    },
                },
            }
        ),
    ],
    db: AsyncSession = Depends(get_db),
    _pet: Pets = Depends(get_current_user_pet),
) -> PetRead:
    pet = await update_pet_service(db, pet_id, pet_update)
    return PetRead.model_validate(pet)


# app/api/v1/pets/{pet_id}
@pets_router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a pet for the current user",
)
async def delete_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    _pet: Pets = Depends(get_current_user_pet),
) -> None:
    await delete_pet_service(db, pet_id)
