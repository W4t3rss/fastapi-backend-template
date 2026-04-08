
from fastapi import APIRouter, Depends, Query, status
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
    get_all_pets_service,
    get_pet_by_id_service,
    update_pet_admin_service,
)
from app.services.users import (
    create_user_admin_service,
    delete_user_service,
    get_all_users_service,
    get_user_by_id_service,
    update_user_admin_service,
)


admini_router = APIRouter()


@admini_router.post(
    "/users",
    response_model=UserReadAdmin,
    status_code=status.HTTP_201_CREATED,
    summary="管理员创建用户",
)
async def create_user_by_admin(
    user_create: UserCreateAdmin,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await create_user_admin_service(db, user_create)
    return UserReadAdmin.model_validate(user)


@admini_router.get(
    "/users",
    response_model=UserPageResponse,
    status_code=status.HTTP_200_OK,
    summary="管理员获取用户列表",
)
async def get_users_by_admin(
    skip: int = Query(default=0, ge=0, description="分页偏移量"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserPageResponse:
    result = await get_all_users_service(db, skip)
    return UserPageResponse.model_validate(result)


@admini_router.get(
    "/users/{user_id}",
    response_model=UserReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="管理员获取单个用户",
)
async def get_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await get_user_by_id_service(db, user_id)
    return UserReadAdmin.model_validate(user)


@admini_router.patch(
    "/users/{user_id}",
    response_model=UserReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="管理员更新用户",
)
async def update_user_by_admin(
    user_id: int,
    user_update: UserUpdateAdmin,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> UserReadAdmin:
    user = await update_user_admin_service(db, user_id, user_update)
    return UserReadAdmin.model_validate(user)


@admini_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="管理员删除用户",
)
async def delete_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> None:
    await delete_user_service(db, user_id, current_admin.id)


@admini_router.post(
    "/pets",
    response_model=PetReadAdmin,
    status_code=status.HTTP_201_CREATED,
    summary="管理员创建宠物",
)
async def create_pet_by_admin(
    pet_create: PetCreateAdmin,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await create_pet_admin_service(db, pet_create)
    return PetReadAdmin.model_validate(pet)


@admini_router.get(
    "/pets",
    response_model=PetAdminPageResponse,
    status_code=status.HTTP_200_OK,
    summary="管理员获取宠物列表",
)
async def get_pets_by_admin(
    skip: int = Query(default=0, ge=0, description="分页偏移量"),
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetAdminPageResponse:
    result = await get_all_pets_service(db, skip)
    return PetAdminPageResponse.model_validate(result)


@admini_router.get(
    "/pets/{pet_id}",
    response_model=PetReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="管理员获取单个宠物",
)
async def get_pet_by_admin(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await get_pet_by_id_service(db, pet_id)
    return PetReadAdmin.model_validate(pet)


@admini_router.patch(
    "/pets/{pet_id}",
    response_model=PetReadAdmin,
    status_code=status.HTTP_200_OK,
    summary="管理员更新宠物",
)
async def update_pet_by_admin(
    pet_id: int,
    pet_update: PetUpdateAdmin,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> PetReadAdmin:
    pet = await update_pet_admin_service(db, pet_id, pet_update)
    return PetReadAdmin.model_validate(pet)


@admini_router.delete(
    "/pets/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="管理员删除宠物",
)
async def delete_pet_by_admin(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Users = Depends(get_current_admin),
) -> None:
    await delete_pet_service(db, pet_id)