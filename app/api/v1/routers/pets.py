
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.exceptions.base import ForbiddenException
from app.models.users import Users
from app.schemas.pets import PetCreate, PetPageResponse, PetRead, PetUpdate
from app.services.pets import (
    create_pet_service,
    delete_pet_service,
    get_pet_by_id_service,
    get_pets_by_owner_id_service,
    update_pet_service,
)


pets_router = APIRouter()


async def _get_current_user_pet(
    pet_id: int,
    db: AsyncSession,
    current_user: Users,
):
    pet = await get_pet_by_id_service(db, pet_id)
    if pet.owner_id != current_user.id:
        raise ForbiddenException(message="You do not have permission to access this pet")
    return pet


@pets_router.post(
    "",
    response_model=PetRead,
    status_code=status.HTTP_201_CREATED,
    summary="创建当前用户的宠物",
)
async def create_pet(
    pet_create: PetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> PetRead:
    pet = await create_pet_service(db, current_user.id, pet_create)
    return PetRead.model_validate(pet)


@pets_router.get(
    "",
    response_model=PetPageResponse,
    status_code=status.HTTP_200_OK,
    summary="获取当前用户的宠物列表",
)
async def get_my_pets(
    skip: int = Query(default=0, ge=0, description="分页偏移量"),
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> PetPageResponse:
    result = await get_pets_by_owner_id_service(db, current_user.id, skip)
    return PetPageResponse.model_validate(result)


@pets_router.get(
    "/{pet_id}",
    response_model=PetRead,
    status_code=status.HTTP_200_OK,
    summary="获取当前用户的单个宠物",
)
async def get_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> PetRead:
    pet = await _get_current_user_pet(pet_id, db, current_user)
    return PetRead.model_validate(pet)


@pets_router.patch(
    "/{pet_id}",
    response_model=PetRead,
    status_code=status.HTTP_200_OK,
    summary="更新当前用户的宠物",
)
async def update_pet(
    pet_id: int,
    pet_update: PetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> PetRead:
    await _get_current_user_pet(pet_id, db, current_user)
    pet = await update_pet_service(db, pet_id, pet_update)
    return PetRead.model_validate(pet)


@pets_router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除当前用户的宠物",
)
async def delete_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> None:
    await _get_current_user_pet(pet_id, db, current_user)
    await delete_pet_service(db, pet_id)