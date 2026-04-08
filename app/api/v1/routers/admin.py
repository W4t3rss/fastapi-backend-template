
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_admin, get_db
from app.models.users import Users
from app.schemas.pets import (
    PetAdminPageResponse,
    PetCreateAdmin,
    PetReadAdmin,
    PetUpdateAdmin,
)
from app.schemas.users import (
    UserCreateAdmin,
    UserPageResponse,
    UserReadAdmin,
    UserUpdateAdmin,
)
from app.services.pets import (
    create_pet_admin_service,
    delete_pet_service,
    get_all_pets_admin_service,
    get_pet_by_id_admin_service,
    restore_pet_service,
    update_pet_admin_service,
)
from app.services.users import (
    create_user_admin_service,
    delete_user_service,
    get_all_users_admin_service,
    get_user_by_id_admin_service,
    restore_user_service,
    update_user_admin_service,
)
admini_router = APIRouter()


# app/api/v1/admin/users
@admini_router.post(
    "/users",
    response_model=UserReadAdmin,
    status_code=status.HTTP_201_CREATED,
    summary="Admin creates a user",
)
async def create_user_by_admin(
    user_create: UserCreateAdmin,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await create_user_admin_service(db, user_create)
    return UserReadAdmin.model_validate(user)


# app/api/v1/admin/users
@admini_router.get(
    "/users",
    response_model=UserPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Admin gets user list",
)
async def get_users_by_admin(
    skip: int = Query(default=0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserPageResponse:
    result = await get_all_users_admin_service(db, skip)
    return UserPageResponse.model_validate(result)


# app/api/v1/admin/users/{user_id}
@admini_router.get(
    "/users/{user_id}",
    response_model=UserReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="Admin gets a single user",
)
async def get_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await get_user_by_id_admin_service(db, user_id)
    return UserReadAdmin.model_validate(user)


# app/api/v1/admin/users/{user_id}
@admini_router.patch(
    "/users/{user_id}",
    response_model=UserReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="Admin updates a user",
)
async def update_user_by_admin(
    user_id: int,
    user_update: Annotated[
        UserUpdateAdmin,
        Body(
            openapi_examples={
                "full_update": {
                    "summary": "Complete example",
                    "value": {
                        "user_name": "user1_new",
                        "phone_number": "13800138001",
                        "password": "87654321",
                        "role": 0,
                    },
                },
                "rename_user": {
                    "summary": "Rename user",
                    "value": {
                        "user_name": "user1_new",
                    },
                },
                "change_phone": {
                    "summary": "Change phone number",
                    "value": {
                        "phone_number": "13800138001",
                    },
                },
                "promote_admin": {
                    "summary": "Change role",
                    "value": {
                        "role": 1,
                    },
                },
                "reset_password": {
                    "summary": "Reset password",
                    "value": {
                        "password": "87654321",
                    },
                },
            }
        ),
    ],
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await update_user_admin_service(db, user_id, user_update)
    return UserReadAdmin.model_validate(user)


# app/api/v1/admin/users/{user_id}
@admini_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Admin deletes a user",
)
async def delete_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> None:
    await delete_user_service(db, user_id, current_admin.id)


# app/api/v1/admin/users/{user_id}/restore
@admini_router.post(
    "/users/{user_id}/restore",
    response_model=UserReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="Admin restores a soft-deleted user",
)
async def restore_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await restore_user_service(db, user_id)
    return UserReadAdmin.model_validate(user)


# app/api/v1/admin/pets
@admini_router.post(
    "/pets",
    response_model=PetReadAdmin,
    status_code=status.HTTP_201_CREATED,
    summary="Admin creates a pet",
)
async def create_pet_by_admin(
    pet_create: PetCreateAdmin,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await create_pet_admin_service(db, pet_create)
    return PetReadAdmin.model_validate(pet)


# app/api/v1/admin/pets
@admini_router.get(
    "/pets",
    response_model=PetAdminPageResponse,
    status_code=status.HTTP_200_OK,
    summary="Admin gets pet list",
)
async def get_pets_by_admin(
    skip: int = Query(default=0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetAdminPageResponse:
    result = await get_all_pets_admin_service(db, skip)
    return PetAdminPageResponse.model_validate(result)


# app/api/v1/admin/pets/{pet_id}
@admini_router.get(
    "/pets/{pet_id}",
    response_model=PetReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="Admin gets a single pet",
)
async def get_pet_by_admin(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await get_pet_by_id_admin_service(db, pet_id)
    return PetReadAdmin.model_validate(pet)


# app/api/v1/admin/pets/{pet_id}
@admini_router.patch(
    "/pets/{pet_id}",
    response_model=PetReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="Admin updates a pet",
)
async def update_pet_by_admin(
    pet_id: int,
    pet_update: Annotated[
        PetUpdateAdmin,
        Body(
            openapi_examples={
                "full_update": {
                    "summary": "Complete example",
                    "value": {
                        "pet_name": "Buddy Jr.",
                        "owner_id": 3,
                    },
                },
                "rename_pet": {
                    "summary": "Rename pet",
                    "value": {
                        "pet_name": "Buddy Jr.",
                    },
                },
                "transfer_owner": {
                    "summary": "Transfer ownership",
                    "value": {
                        "owner_id": 3,
                    },
                },
            }
        ),
    ],
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await update_pet_admin_service(db, pet_id, pet_update)
    return PetReadAdmin.model_validate(pet)


# app/api/v1/admin/pets/{pet_id}
@admini_router.delete(
    "/pets/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Admin deletes a pet",
)
async def delete_pet_by_admin(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> None:
    await delete_pet_service(db, pet_id)


# app/api/v1/admin/pets/{pet_id}/restore
@admini_router.post(
    "/pets/{pet_id}/restore",
    response_model=PetReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="Admin restores a soft-deleted pet",
)
async def restore_pet_by_admin(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await restore_pet_service(db, pet_id)
    return PetReadAdmin.model_validate(pet)
