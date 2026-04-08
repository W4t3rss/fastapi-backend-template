
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.base import AppBaseException
from app.models.users import Users
from app.schemas.users import (UserCreate, UserCreateAdmin, UserUpdate, UserUpdateAdmin)
from app.crud import * 
from app.exceptions import *
from app.core.security import create_password_hash
from app.core.lifespan import logger


# Create
async def create_user_service(db: AsyncSession, user_create: UserCreate) -> Users:
    try:
        # 校验
        if await get_user_by_user_name(db, user_create.user_name):
            logger.warning("Create user failed: username already exists, user_name={}", user_create.user_name)
            raise UsernameAlreadyExistsException()
        
        if user_create.phone_number and await get_user_by_phone_number(db, user_create.phone_number):
            logger.warning("Create user failed: phone number already exists, phone_number={}", user_create.phone_number)
            raise PhoneAlreadyExistsException()
        
        # 业务逻辑处理
        hashed_password = create_password_hash(user_create.password)
        user_create_hashed = user_create.model_copy(update={"password": hashed_password})  

        # 数据库写入
        user = await create_user(db, user_create_hashed)
        await db.commit()

        logger.info(
            f"User created successfully: id={user.id}, user_name={user.user_name}, phone_number={user.phone_number}"
        )
        return user

    except AppBaseException:
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error: {}", e)
        raise


async def create_user_admin_service(db: AsyncSession, user_create: UserCreateAdmin) -> Users:
    try:
        # 校验
        if await get_user_by_user_name(db, user_create.user_name):
            logger.warning("Create admin user failed: username already exists, user_name={}", user_create.user_name)
            raise UsernameAlreadyExistsException()
        
        if user_create.phone_number and await get_user_by_phone_number(db, user_create.phone_number):
            logger.warning("Create admin user failed: phone number already exists, phone_number={}", user_create.phone_number)
            raise PhoneAlreadyExistsException()
        
        hashed_password = create_password_hash(user_create.password)
        user_create_hashed = user_create.model_copy(update={"password": hashed_password})

        user = await create_user_admin(db, user_create_hashed)
        await db.commit()

        logger.info(
            f"Admin user created successfully: id={user.id}, user_name={user.user_name}, phone_number={user.phone_number}"
        )
        return user

    except AppBaseException:
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error: {}", e)
        raise


# Read
async def get_user_by_id_service(db: AsyncSession, user_id: int) -> Users:
    user = await get_user_by_id(db, user_id)
    if user is None:
        logger.warning("Get user by ID failed: user not found, user_id={}", user_id)
        raise UserNotFoundException()
    logger.info("Get user by ID succeeded: user_id={}, user_name={}", user.id, user.user_name)
    return user


async def get_user_by_user_name_service(db: AsyncSession, user_name: str) -> Users:
    user = await get_user_by_user_name(db, user_name)
    if user is None:
        logger.warning("Get user by username failed: user not found, user_name={}", user_name)
        raise UserNotFoundException()
    logger.info("Get user by username succeeded: user_id={}, user_name={}", user.id, user.user_name)
    return user


async def get_user_by_phone_number_service(db: AsyncSession, phone_number: str) -> Users:
    user = await get_user_by_phone_number(db, phone_number)
    if user is None:
        logger.warning("Get user by phone number failed: user not found, phone_number={}", phone_number)
        raise UserNotFoundException()
    logger.info("Get user by phone number succeeded: user_id={}, phone_number={}", user.id, user.phone_number)
    return user


async def get_user_by_id_admin_service(db: AsyncSession, user_id: int) -> Users:
    user = await get_user_by_id_including_deleted(db, user_id)
    if user is None:
        logger.warning("Admin get user by ID failed: user not found, user_id={}", user_id)
        raise UserNotFoundException()
    logger.info(
        "Admin fetched user by ID: user_id={}, user_name={}, is_deleted={}",
        user.id,
        user.user_name,
        user.is_deleted,
    )
    return user


async def get_all_users_admin_service(db: AsyncSession, skip: int = 0) -> dict:
    result = await get_all_users_including_deleted(db, skip)
    logger.info(
        "Admin listed users: total={}, page={}, limit={}",
        result.get("total"),
        result.get("page"),
        result.get("limit"),
    )
    return result


# Update
async def update_user_service(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Users:
    try:
        user = await get_user_by_id(db, user_id)
        if user is None:
            logger.warning("Update user failed: user not found, user_id={}", user_id)
            raise UserNotFoundException()

        # 检查用户名/手机号冲突
        if user_update.user_name:
            existing = await get_user_by_user_name(db, user_update.user_name)
            if existing and existing.id != user_id:
                logger.warning(
                    "Update user failed: user_name already exists, user_id={}, user_name={}",
                    user_id,
                    user_update.user_name,
                )
                raise UsernameAlreadyExistsException()

        if user_update.phone_number:
            existing = await get_user_by_phone_number(db, user_update.phone_number)
            if existing and existing.id != user_id:
                logger.warning(
                    "Update user failed: phone_number already exists, user_id={}, phone_number={}",
                    user_id,
                    user_update.phone_number,
                )
                raise PhoneAlreadyExistsException()

        if user_update.password is not None:
            hashed_password = create_password_hash(user_update.password)
            user_update = user_update.model_copy(update={"password": hashed_password})

        updated_user = await update_user(db, user_id, user_update)
        if updated_user is None:
            logger.warning("Update user failed: user not found after validation, user_id={}", user_id)
            raise UserNotFoundException()

        await db.commit()
        logger.info("User updated: user_id={}, user_name={}", updated_user.id, updated_user.user_name)
        return updated_user

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during user update: {}", e)
        raise


async def update_user_admin_service(db: AsyncSession, user_id: int, user_update: UserUpdateAdmin) -> Users:
    try:
        user = await get_user_by_id(db, user_id)
        if user is None:
            logger.warning("Update admin user failed: user not found, user_id={}", user_id)
            raise UserNotFoundException()

        if user_update.user_name:
            existing = await get_user_by_user_name(db, user_update.user_name)
            if existing and existing.id != user_id:
                logger.warning(
                    "Update admin user failed: user_name already exists, user_id={}, user_name={}",
                    user_id,
                    user_update.user_name,
                )
                raise UsernameAlreadyExistsException()

        if user_update.phone_number:
            existing = await get_user_by_phone_number(db, user_update.phone_number)
            if existing and existing.id != user_id:
                logger.warning(
                    "Update admin user failed: phone_number already exists, user_id={}, phone_number={}",
                    user_id,
                    user_update.phone_number,
                )
                raise PhoneAlreadyExistsException()

        if user_update.password is not None:
            hashed_password = create_password_hash(user_update.password)
            user_update = user_update.model_copy(update={"password": hashed_password})

        updated_user = await update_user_admin(db, user_id, user_update)
        if updated_user is None:
            logger.warning("Update admin user failed: user not found after validation, user_id={}", user_id)
            raise UserNotFoundException()

        await db.commit()
        logger.info("Admin user updated: user_id={}, user_name={}", updated_user.id, updated_user.user_name)
        return updated_user

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during admin user update: {}", e)
        raise


# Delete
async def delete_user_service(db: AsyncSession, user_id: int, current_user_id: int) -> None:
    """删除用户"""
    try:
        user = await get_user_by_id(db, user_id)
        if user is None:
            logger.warning("Delete user failed: user not found, user_id={}", user_id)
            raise UserNotFoundException()

        if current_user_id == user_id:
            logger.warning("Delete user failed: cannot delete self, user_id={}", user_id)
            raise CannotDeleteSelfException()

        await delete_user(db, user_id)
        await db.commit()
        logger.info("User deleted: user_id={}, user_name={}", user.id, user.user_name)

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during user deletion: {}", e)
        raise


async def restore_user_service(db: AsyncSession, user_id: int) -> Users:
    try:
        user = await get_user_by_id_including_deleted(db, user_id)
        if user is None:
            logger.warning("Restore user failed: user not found, user_id={}", user_id)
            raise UserNotFoundException()

        if not user.is_deleted:
            logger.info("Restore user skipped: user already active, user_id={}, user_name={}", user.id, user.user_name)
            return user

        restored_user = await restore_user(db, user_id)
        if restored_user is None:
            logger.warning("Restore user failed after validation: user not found, user_id={}", user_id)
            raise UserNotFoundException()

        await db.commit()
        logger.info("User restored: user_id={}, user_name={}", restored_user.id, restored_user.user_name)
        return restored_user

    except AppBaseException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during user restoration: {}", e)
        raise
