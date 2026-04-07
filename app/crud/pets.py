
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pets import Pets
from app.schemas.pets import (PetCreate,
                              PetUpdate, PetUpdateAdmin
                              )
from sqlalchemy import func, select
from app.core.config.db_cfg import get_db_cfg
db_cfg = get_db_cfg()


# Create
async def create_pet(db: AsyncSession, pet_create: PetCreate) -> Pets:
    """
    创建宠物
    param db: 数据库会话
    param pet_create: 宠物创建数据
    return: 创建的宠物数据
    """
    pet = Pets(
        pet_name=pet_create.pet_name,
        owner_id=pet_create.owner_id
    )
    db.add(pet)
    await db.flush()
    await db.refresh(pet)
    return pet


# Read
async def get_pet_by_id(db: AsyncSession, pet_id: int) -> Pets | None:
    """
    根据ID获取宠物
    param db: 数据库会话
    param pet_id: 宠物ID
    return: 宠物数据
    """
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_id, 
            Pets.is_deleted == False
        )
    )
    pet = result.scalar_one_or_none()
    if pet is None:
        return None
    return pet


async def get_pet_by_pet_name(db: AsyncSession, pet_name: str) -> Pets | None:
    """
    根据宠物名称获取宠物
    param db: 数据库会话
    param pet_name: 宠物名称
    return: 宠物数据
    """
    result = await db.execute(
        select(Pets)
        .where(
            Pets.pet_name == pet_name, 
            Pets.is_deleted == False
        )
    )
    pet = result.scalar_one_or_none()
    if pet is None:
        return None
    return pet


async def get_pets_by_owner_id(db: AsyncSession, owner_id: int, skip: int = 0) -> dict:
    """
    根据主人ID获取宠物列表
    param db: 数据库会话
    param owner_id: 主人ID
    param skip: 跳过的记录数
    return: 包含宠物列表和分页信息的字典
    """

    skip = skip if skip >= 0 else 0
    limit = db_cfg.LIMIT

    result = await db.execute(
        select(Pets)
        .where(
            Pets.owner_id == owner_id, 
            Pets.is_deleted == False
        )
        .offset(skip)
        .limit(limit)
        .order_by(Pets.id)
    )
    pets = result.scalars().all()

    count_result = await db.execute(
        select(func.count(Pets.id))
        .where(
            Pets.owner_id == owner_id,
            Pets.is_deleted == False
        )
    )
    total = count_result.scalar()

    return {
        "items": [pet for pet in pets],
        "total": total,
        "page": (skip // limit) + 1,
        "pages": max(1, (total + limit - 1) // limit),
        "limit": limit
    }

async def get_all_pets(db: AsyncSession, skip: int=0) -> dict:
    """
    获取所有宠物
    param db: 数据库会话
    param skip: 跳过的记录数
    return: 包含宠物列表和分页信息的字典
    """
    skip = skip if skip >= 0 else 0
    limit = db_cfg.LIMIT

    result = await db.execute(
        select(Pets)
        .where(Pets.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .order_by(Pets.id)
    )
    pets = result.scalars().all()

    count_result = await db.execute(
        select(func.count(Pets.id)).where(Pets.is_deleted == False)
    )
    total = count_result.scalar()

    return {
        "items": [pet for pet in pets],
        "total": total,
        "page": (skip // limit) + 1,
        "pages": max(1, (total + limit - 1) // limit),
        "limit": limit
    }


# Update
async def update_pet(db: AsyncSession, pet_id: int, pet_update: PetUpdate) -> Pets | None:
    """
    更新宠物信息
    param db: 数据库会话
    param pet_update: 宠物更新数据
    return: 更新后的宠物数据
    """
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_id,
            Pets.is_deleted == False
        )
    )
    pet = result.scalar_one_or_none()
    if pet is None:
        return None

    if pet_update.pet_name is not None:
        pet.pet_name = pet_update.pet_name

    await db.flush()
    await db.refresh(pet)
    return pet


async def update_pet_admin(db: AsyncSession, pet_id: int, pet_update: PetUpdateAdmin) -> Pets | None:
    """
    更新宠物信息（管理员）
    param db: 数据库会话
    param pet_update: 宠物更新数据
    return: 更新后的宠物数据
    """
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_id, 
            Pets.is_deleted == False
        )
    )
    pet = result.scalar_one_or_none()
    if pet is None:
        return None

    if pet_update.pet_name is not None:
        pet.pet_name = pet_update.pet_name

    if pet_update.owner_id is not None:
        pet.owner_id = pet_update.owner_id

    await db.flush()
    await db.refresh(pet)
    return pet


# Delete
async def delete_pet(db: AsyncSession, pet_id: int) -> Pets | None:
    """
    软删除宠物
    param db: 数据库会话
    param pet_id: 宠物ID
    return: 删除的宠物数据
    """
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_id, 
            Pets.is_deleted == False
        )
    )           
    pet = result.scalar_one_or_none()
    if pet is None:
        return None

    pet.is_deleted = True
    await db.flush()
    await db.refresh(pet)
    return pet

