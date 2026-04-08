
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.pets import create_pet_admin
from app.exceptions.base import AppBaseException
from app.models.pets import Pets
from app.schemas.pets import (PetCreate, PetUpdate, PetCreateAdmin, PetUpdateAdmin)
from app.crud import * 
from app.exceptions import *
from app.core.lifespan import logger


# Create
async def create_pet_service(db: AsyncSession, owner_id: int, pet_create: PetCreate) -> Pets:
    try:
        # 校验
        if await get_user_by_id(db, owner_id) is None:
            logger.warning("Create pet failed: owner not found, owner_id={}", owner_id)
            raise UserNotFoundException()
        if await get_pet_by_pet_name_and_owner_id(db, pet_create.pet_name, owner_id):
            logger.warning(
                "Create pet failed: pet already exists, owner_id={}, pet_name={}",
                owner_id,
                pet_create.pet_name,
            )
            raise PetAlreadyExistsException()
        pet_create_admin = PetCreateAdmin(
            owner_id=owner_id,
            pet_name=pet_create.pet_name,
        )
        pet = await create_pet_admin(db, pet_create_admin)
        await db.commit()

        logger.info(
            f"Pet created: id={pet.id}, pet_name={pet.pet_name}, owner_id={pet.owner_id}"
        )
        
        return pet

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during pet creation: {}", e)
        raise


async def create_pet_admin_service(db: AsyncSession, pet_create: PetCreateAdmin) -> Pets:
    try:
        # 校验
        if await get_user_by_id(db, pet_create.owner_id) is None:
            logger.warning("Create pet admin failed: owner not found, owner_id={}", pet_create.owner_id)
            raise UserNotFoundException()  
        if await get_pet_by_pet_name_and_owner_id(db, pet_create.pet_name, pet_create.owner_id):
            logger.warning(
                "Create pet admin failed: pet already exists, owner_id={}, pet_name={}",
                pet_create.owner_id,
                pet_create.pet_name,
            )
            raise PetAlreadyExistsException()
        
        pet = await create_pet_admin(db, pet_create)
        await db.commit()

        logger.info(
            f"Pet created: id={pet.id}, pet_name={pet.pet_name}, owner_id={pet.owner_id}"
        )
        return pet

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during pet creation: {}", e)
        raise


# Read
async def get_pet_by_id_service(db: AsyncSession, pet_id: int) -> Pets:
    pet = await get_pet_by_id(db, pet_id)
    if not pet:
        logger.warning("Get pet by id failed: pet not found, pet_id={}", pet_id)
        raise PetNotFoundException()
    logger.info("Pet fetched by id: pet_id={}, owner_id={}, pet_name={}", pet.id, pet.owner_id, pet.pet_name)
    return pet


async def get_pets_by_owner_id_service(db: AsyncSession, owner_id: int, skip: int = 0) -> dict:
    user = await get_user_by_id(db, owner_id)
    if not user:
        logger.warning("Get pets by owner id failed: owner not found, owner_id={}", owner_id)
        raise UserNotFoundException()
    result = await get_pets_by_owner_id(db, owner_id, skip)
    logger.info(
        "Pets fetched by owner id: owner_id={}, total={}",
        owner_id,
        result.get("total"),
    )
    return result


async def get_pet_by_pet_name_and_owner_id_service(db: AsyncSession, pet_name: str, owner_id: int) -> Pets:
    user = await get_user_by_id(db, owner_id)
    if not user:
        logger.warning("Get pet by name failed: owner not found, owner_id={}", owner_id)
        raise UserNotFoundException()
    pet = await get_pet_by_pet_name_and_owner_id(db, pet_name, owner_id)
    if not pet:
        logger.warning(
            "Get pet by name failed: pet not found, owner_id={}, pet_name={}",
            owner_id,
            pet_name,
        )
        raise PetNotFoundException()
    logger.info("Pet fetched by name: pet_id={}, owner_id={}, pet_name={}", pet.id, pet.owner_id, pet.pet_name)
    return pet


async def get_all_pets_service(db: AsyncSession, skip: int = 0) -> dict:
    result = await get_all_pets(db, skip)
    logger.info(
        "Pets listed: total={}, page={}, limit={}",
        result.get("total"),
        result.get("page"),
        result.get("limit"),
    )
    return result


# Update
async def update_pet_service(db: AsyncSession, pet_id: int, pet_update: PetUpdate) -> Pets:
    try:
        pet = await get_pet_by_id(db, pet_id)
        if not pet:
            logger.warning("Update pet failed: pet not found, pet_id={}", pet_id)
            raise PetNotFoundException()

        if pet_update.pet_name:
            existing_pet = await get_pet_by_pet_name_and_owner_id(db, pet_update.pet_name, pet.owner_id)
            if existing_pet and existing_pet.id != pet_id:
                logger.warning(
                    "Update pet failed: pet_name already exists, pet_id={}, owner_id={}, pet_name={}",
                    pet_id,
                    pet.owner_id,
                    pet_update.pet_name,
                )
                raise PetAlreadyExistsException()

        updated_pet = await update_pet(db, pet_id, pet_update)
        if not updated_pet:
            logger.warning("Update pet failed: pet not found after validation, pet_id={}", pet_id)
            raise PetNotFoundException()

        await db.commit()
        logger.info(
            "Pet updated: pet_id={}, owner_id={}, pet_name={}",
            updated_pet.id,
            updated_pet.owner_id,
            updated_pet.pet_name,
        )
        return updated_pet

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during pet update: {}", e)
        raise


async def update_pet_admin_service(db: AsyncSession, pet_id: int, pet_update: PetUpdateAdmin) -> Pets:
    try:
        user = await get_user_by_id(db, pet_update.owner_id) if pet_update.owner_id else None
        if pet_update.owner_id and not user:
            logger.warning("Update pet admin failed: owner not found, owner_id={}", pet_update.owner_id)
            raise UserNotFoundException()

        pet = await get_pet_by_id(db, pet_id)
        if not pet:
            logger.warning("Update pet admin failed: pet not found, pet_id={}", pet_id)
            raise PetNotFoundException()

        target_owner_id = pet_update.owner_id if pet_update.owner_id is not None else pet.owner_id
        target_pet_name = pet_update.pet_name if pet_update.pet_name is not None else pet.pet_name
        existing_pet = await get_pet_by_pet_name_and_owner_id(db, target_pet_name, target_owner_id)
        if existing_pet and existing_pet.id != pet_id:
            logger.warning(
                "Update pet admin failed: pet_name already exists, pet_id={}, owner_id={}, pet_name={}",
                pet_id,
                target_owner_id,
                target_pet_name,
            )
            raise PetAlreadyExistsException()

        updated_pet = await update_pet_admin(db, pet_id, pet_update)
        if not updated_pet:
            logger.warning("Update pet admin failed: pet not found after validation, pet_id={}", pet_id)
            raise PetNotFoundException()

        await db.commit()
        logger.info(
            "Pet admin updated: pet_id={}, owner_id={}, pet_name={}",
            updated_pet.id,
            updated_pet.owner_id,
            updated_pet.pet_name,
        )
        return updated_pet

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during pet admin update: {}", e)
        raise


# Delete
async def delete_pet_service(db: AsyncSession, pet_id: int) -> None:
    try:
        pet = await get_pet_by_id(db, pet_id)
        if not pet:
            logger.warning("Delete pet failed: pet not found, pet_id={}", pet_id)
            raise PetNotFoundException()

        await delete_pet(db, pet_id)
        await db.commit()
        logger.info("Pet deleted: pet_id={}, owner_id={}, pet_name={}", pet.id, pet.owner_id, pet.pet_name)

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during pet deletion: {}", e)
        raise




