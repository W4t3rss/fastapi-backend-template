
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.base import AppBaseException
from app.models.users import Users
from app.schemas.users import (UserCreate, UserCreateAdmin, UserUpdate, UserUpdateAdmin)
from app.crud import * 
from app.exceptions import *
from app.core.security import create_password_hash
from app.utils import logger


# Create
async def create_user_service(db: AsyncSession, user_create: UserCreate) -> Users:
    """创建普通用户"""
    try:
        # 校验
        if await get_user_by_user_name(db, user_create.user_name):
            raise UsernameAlreadyExistsException()
        
        if user_create.phone_number and await get_user_by_phone_number(db, user_create.phone_number):
            raise PhoneAlreadyExistsException()
        
        # 业务逻辑处理
        hashed_password = create_password_hash(user_create.password)
        # 创建一个新的UserCreate对象，替换原始密码为哈希后的密码
        user_create_hashed = user_create.model_copy(update={"password": hashed_password})  

        # 数据库写入
        user = await create_user(db, user_create_hashed)
        await db.commit()

        logger.info(
            f"User created: id={user.id}, user_name={user.user_name}, phone_number={user.phone_number}"
        )
        return user

    except AppBaseException:
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during user creation: {}", e)
        raise


async def create_user_admin_service(db: AsyncSession, user_create: UserCreateAdmin) -> Users:
    """创建管理员用户"""
    try:
        # 校验
        if await get_user_by_user_name(db, user_create.user_name):
            raise UsernameAlreadyExistsException()
        
        if user_create.phone_number and await get_user_by_phone_number(db, user_create.phone_number):
            raise PhoneAlreadyExistsException()
        
        hashed_password = create_password_hash(user_create.password)
        user_create_hashed = user_create.model_copy(update={"password": hashed_password})

        user = await create_user_admin(db, user_create_hashed)
        await db.commit()

        logger.info(
            f"Admin user created: id={user.id}, user_name={user.user_name}, phone_number={user.phone_number}"
        )
        return user

    except AppBaseException:
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error during admin user creation: {}", e)
        raise


# Read
async def get_user_by_id_service(db: AsyncSession, user_id: int) -> Users:
    """根据ID获取用户"""
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundException()
    return user


async def get_user_by_user_name_service(db: AsyncSession, user_name: str) -> Users:
    """根据用户名获取用户"""
    user = await get_user_by_user_name(db, user_name)
    if user is None:
        raise UserNotFoundException()
    return user


async def get_user_by_phone_number_service(db: AsyncSession, phone_number: str) -> Users:
    """根据手机号获取用户"""
    user = await get_user_by_phone_number(db, phone_number)
    if user is None:
        raise UserNotFoundException()
    return user


async def get_all_users_service(db: AsyncSession) -> dict:
    """获取所有用户（带分页）"""
    return await get_all_users(db)


# Update
async def update_user_service(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Users:
    """更新普通用户"""
    user = await get_user_by_id(db, user_id)  
    if user is None:
        raise UserNotFoundException()
    
    # 检查用户名/手机号冲突
    if user_update.user_name:
        existing = await get_user_by_user_name(db, user_update.user_name)
        if existing and existing.id != user_id:
            raise UsernameAlreadyExistsException()

    if user_update.phone_number:
        existing = await get_user_by_phone_number(db, user_update.phone_number)
        if existing and existing.id != user_id:
            raise PhoneAlreadyExistsException()

    user = await update_user(db, user_id, user_update)
    await db.commit()   
    return user


async def update_user_admin_service(db: AsyncSession, user_id: int, user_update: UserUpdateAdmin) -> Users:
    """更新管理员用户"""
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundException()
    
    if user_update.user_name:
        existing = await get_user_by_user_name(db, user_update.user_name)
        if existing and existing.id != user_id:
            raise UsernameAlreadyExistsException()

    if user_update.phone_number:
        existing = await get_user_by_phone_number(db, user_update.phone_number)
        if existing and existing.id != user_id:
            raise PhoneAlreadyExistsException()

    user = await update_user_admin(db, user_id, user_update)
    await db.commit()   
    return user


# Delete
async def delete_user_service(db: AsyncSession, user_id: int, current_user_id: int) -> None:
    """删除用户"""
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundException()

    if current_user_id == user_id:
        raise CannotDeleteSelfException()

    await delete_user(db, user_id)
    await db.commit()