
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pets import Pets
from app.schemas.pets import (PetCreate,
                              PetRead,PetReadAdmin,
                              PetUpdate, PetUpdateAdmin
                              )
from sqlalchemy import func, select
from app.core.config.db_cfg import get_db_cfg
db_cfg = get_db_cfg()


# Create
async def create_pet(db: AsyncSession, pet_create: PetCreate) -> PetRead:
    pet = Pets(
        name=pet_create.name,
        age=pet_create.age,
        type=pet_create.type,
        owner_id=pet_create.owner_id
    )
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return PetRead.model_validate(pet)


# Read
async def get_pet_by_id(db: AsyncSession, pet_id: int) -> PetReadAdmin | None:
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
    return PetReadAdmin.model_validate(pet)


async def get_pet_by_owner_id(db: AsyncSession, owner_id: int) -> dict:

    skip = db_cfg.SKIP
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
        "items": [PetReadAdmin.model_validate(pet) for pet in pets],
        "total": total,
        "page": (total - 1) // limit + 1,
        "pages": (total - 1) // limit + 1,
        "limit": limit
    }

async def get_all_pets(db: AsyncSession) -> dict:
    skip = db_cfg.SKIP
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
        "items": [PetReadAdmin.model_validate(pet) for pet in pets],
        "total": total,
        "page": (total - 1) // limit + 1,
        "pages": (total - 1) // limit + 1,
        "limit": limit
    }


# Update
async def update_pet(db: AsyncSession, pet_update: PetUpdate) -> PetRead | None:
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_update.id, 
            Pets.is_deleted == False
        )
    )
    pet = result.scalar_one_or_none()
    if pet is None:
        return None

    if pet_update.pet_name is not None:
        pet.pet_name = pet_update.pet_name

    await db.commit()
    await db.refresh(pet)
    return PetRead.model_validate(pet)


async def update_pet_admin(db: AsyncSession, pet_update: PetUpdateAdmin) -> PetReadAdmin | None:
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_update.id, 
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

    await db.commit()
    await db.refresh(pet)
    return PetReadAdmin.model_validate(pet)


# Delete
async def delete_pet(db: AsyncSession, pet_id: int) -> bool:
    result = await db.execute(
        select(Pets)
        .where(
            Pets.id == pet_id, 
            Pets.is_deleted == False
        )
    )           
    pet = result.scalar_one_or_none()
    if pet is None:
        return False

    pet.is_deleted = True
    await db.commit()
    return True

