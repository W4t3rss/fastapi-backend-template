
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import Users
from app.schemas.users import (UserCreate,UserCreateAdmin,
                               UserUpdate, UserUpdateAdmin
                               )
from sqlalchemy import func, select
from app.core.config.db_cfg import get_db_cfg
db_cfg = get_db_cfg()


# Create
async def create_user(db: AsyncSession, user_create: UserCreate) -> Users:
    """
    创建用户
    param db: 数据库会话    
    param user_create: 用户创建数据
    return: 创建的用户数据
    """
    user = Users(
        user_name=user_create.user_name,
        phone_number=user_create.phone_number,
        password=user_create.password  # 哈希后的密码
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def create_user_admin(db: AsyncSession, user_create: UserCreateAdmin) -> Users:
    """
    创建用户（管理员）
    param db: 数据库会话    
    param user_create: 用户创建数据
    return: 创建的用户数据
    """
    user = Users(
        role=user_create.role,
        user_name=user_create.user_name,
        phone_number=user_create.phone_number,
        password=user_create.password  # 哈希后的密码
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


# Read
async def get_user_by_id(db: AsyncSession, user_id: int) -> Users | None:
    """
    根据ID获取用户
    param db: 数据库会话
    param user_id: 用户ID
    return: 用户数据
    """
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_id, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return user


async def get_user_by_user_name(db: AsyncSession, user_name: str) -> Users | None:
    """
    根据用户名获取用户
    param db: 数据库会话
    param user_name: 用户名
    return: 用户数据
    """
    result = await db.execute(
        select(Users)
        .where(
            Users.user_name == user_name, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return user 


async def get_user_by_phone_number(db: AsyncSession, phone_number: str) -> Users | None:
    """
    根据电话号码获取用户
    param db: 数据库会话
    param phone_number: 电话号码
    return: 用户数据
    """
    result = await db.execute(
        select(Users)
        .where(
            Users.phone_number == phone_number, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return user


async def get_all_users(db: AsyncSession,skip:int=0) -> dict:
    """
    获取所有用户（分页）
    param db: 数据库会话
    param skip: 跳过的记录数
    return: 包含用户列表和分页信息的字典
    """
    skip = skip if skip >= 0 else 0
    limit = db_cfg.LIMIT
    result = await db.execute(
        select(Users)
        .where(Users.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .order_by(Users.id)
    )
    users = result.scalars().all()

    count_result = await db.execute(
        select(func.count(Users.id)).where(Users.is_deleted == False)
    )
    total = count_result.scalar()
    
    return {
        "items": [user for user in users],
        "total": total,
        "page": (skip // limit) + 1,
        "pages": max(1, (total + limit - 1) // limit),
        "limit": limit   
    }


# Update
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Users | None:
    """
    更新用户信息
    param db: 数据库会话
    param user_update: 用户更新数据
    return: 更新后的用户数据
    """
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_id, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    if user_update.user_name is not None:
        user.user_name = user_update.user_name
    if user_update.phone_number is not None:
        user.phone_number = user_update.phone_number
    if user_update.password is not None:
        user.password = user_update.password  # 哈希后的密码

    await db.flush()
    await db.refresh(user)
    return user

async def update_user_admin(db: AsyncSession, user_id: int, user_update: UserUpdateAdmin) -> Users | None:
    """
    更新用户信息（管理员）
    param db: 数据库会话
    param user_update: 用户更新数据
    return: 更新后的用户数据
    """
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_id, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    if user_update.user_name is not None:
        user.user_name = user_update.user_name
    if user_update.phone_number is not None:
        user.phone_number = user_update.phone_number
    if user_update.password is not None:
        user.password = user_update.password
    if user_update.role is not None:
        user.role = user_update.role

    await db.flush()
    await db.refresh(user)
    return user


# Delete
async def delete_user(db: AsyncSession, user_id: int) -> Users | None:
    """
    软删除用户
    param db: 数据库会话    
    param user_id: 用户ID
    return: 删除的用户数据   
    """
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_id, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    user.is_deleted = True
    await db.flush()
    await db.refresh(user)
    return user
