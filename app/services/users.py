
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users import get_user_by_user_name
from app.exceptions.base import AppBaseException
from app.models.users import Users
from app.schemas.users import (UserCreate,UserCreateAdmin,UserUpdate,UserUpdateAdmin)
from app.crud import * 
from app.exceptions import *
from app.core.security import create_password_hash
from app.utils import logger


# Create
async def create_user_service(db: AsyncSession, user_create: UserCreate) -> Users:
    """
    创建用户
    param db: 数据库会话    
    param user_create: 用户创建数据
    return: 创建的用户数据
    """
    try:
        # 校验
        if await get_user_by_user_name(db, user_create.user_name):
            raise UsernameAlreadyExistsException()
        
        if await get_user_by_phone_number(db, user_create.phone_number):
            raise PhoneAlreadyExistsException()
        
        # 业务逻辑处理
        hashed_password = create_password_hash(user_create.password)
        user_create.password = hashed_password

        # 数据库写入
        user = await create_user(db, user_create)
        await db.commit()

        # 日志
        logger.info(
            f"User created: id={user.id}, user_name={user.user_name}, phone_number={user.phone_number}"
        )

        return user

    # handler 
    except AppBaseException:
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        raise


async def create_user_admin_service(db: AsyncSession, user_create: UserCreateAdmin) -> Users:
    """
    创建用户（管理员）
    param db: 数据库会话    
    param user_create: 用户创建数据
    return: 创建的用户数据
    """
    try:
        # 校验
        if await get_user_by_user_name(db, user_create.user_name):
            raise UsernameAlreadyExistsException()
        
        if await get_user_by_phone_number(db, user_create.phone_number):
            raise PhoneAlreadyExistsException()
        
        # 业务逻辑处理
        hashed_password = create_password_hash(user_create.password)
        user_create.password = hashed_password

        # 数据库写入
        user = await create_user_admin(db, user_create)
        await db.commit()

        # 日志
        logger.info(
            f"User created: id={user.id}, user_name={user.user_name}, phone_number={user.phone_number}"
        )

        return user

    # handler 
    except AppBaseException:
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        raise


# Read
async def get_user_by_id_service(db: AsyncSession, user_id: int) -> Users | None:
    """
    根据ID获取用户
    param db: 数据库会话
    param user_id: 用户ID
    return: 用户数据
    """
    if await get_user_by_id(db, user_id) is None:
        raise UserNotFoundException()
    return await get_user_by_id(db, user_id)

async def get_user_by_user_name_service(db: AsyncSession, user_name: str) -> Users | None:
    """
    根据用户名获取用户
    param db: 数据库会话
    param user_name: 用户名
    return: 用户数据
    """
    if await get_user_by_user_name(db, user_name) is None:
        raise UserNotFoundException()
    return await get_user_by_user_name(db, user_name)


async def get_user_by_phone_number_service(db: AsyncSession, phone_number: str) -> Users | None:
    """
    根据手机号获取用户
    param db: 数据库会话
    param phone_number: 手机号
    return: 用户数据
    """
    if await get_user_by_phone_number(db, phone_number) is None:
        raise UserNotFoundException()
    return await get_user_by_phone_number(db, phone_number)


async def get_all_users_service(db: AsyncSession) -> list[Users]:
    """
    获取所有用户
    param db: 数据库会话
    return: 用户数据列表
    """
    return await get_all_users(db)


# Update
async def update_user_service(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Users:
    """
    更新用户
    param db: 数据库会话
    param user_id: 用户ID
    param user_update: 用户更新数据
    return: 更新后的用户数据
    """
    if await get_user_by_id(db, user_id) is None:
        raise UserNotFoundException()
    
    # 如果更新了用户名，检查新用户名是否已存在
    if user_update.user_name:
        existing_user = await get_user_by_user_name(db, user_update.user_name)
        if existing_user and existing_user.id != user_id:
            raise UsernameAlreadyExistsException()

    # 如果更新了手机号，检查新手机号是否已存在
    if user_update.phone_number:
        existing_user = await get_user_by_phone_number(db, user_update.phone_number)
        if existing_user and existing_user.id != user_id:
            raise PhoneAlreadyExistsException()

    user = await update_user(db, user_id, user_update)
    await db.commit()   
    return user


async def update_user_admin_service(db: AsyncSession, user_id: int, user_update: UserUpdateAdmin) -> Users:
    """
    更新用户（管理员）
    param db: 数据库会话
    param user_id: 用户ID
    param user_update: 用户更新数据
    return: 更新后的用户数据
    """
    if await get_user_by_id(db, user_id) is None:
        raise UserNotFoundException()
    
    # 如果更新了用户名，检查新用户名是否已存在
    if user_update.user_name:
        existing_user = await get_user_by_user_name(db, user_update.user_name)
        if existing_user and existing_user.id != user_id:
            raise UsernameAlreadyExistsException()

    # 如果更新了手机号，检查新手机号是否已存在
    if user_update.phone_number:
        existing_user = await get_user_by_phone_number(db, user_update.phone_number)
        if existing_user and existing_user.id != user_id:
            raise PhoneAlreadyExistsException()

    user = await update_user_admin(db, user_id, user_update)
    await db.commit()   
    return user


# Delete
async def delete_user_service(db: AsyncSession, user_id: int) -> None:
    """
    删除用户
    param db: 数据库会话
    param user_id: 用户ID
    return: None
    """
    if await get_user_by_id(db, user_id) is None:
        raise UserNotFoundException()
    
    await delete_user(db, user_id)
    await db.commit()




