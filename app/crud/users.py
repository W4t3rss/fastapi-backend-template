
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


async def get_user_by_id_including_deleted(db: AsyncSession, user_id: int) -> Users | None:
    result = await db.execute(
        select(Users)
        .where(Users.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return user


async def get_user_by_user_name(db: AsyncSession, user_name: str) -> Users | None:
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


async def get_all_users_including_deleted(db: AsyncSession, skip: int = 0) -> dict:
    skip = skip if skip >= 0 else 0
    limit = db_cfg.LIMIT
    result = await db.execute(
        select(Users)
        .offset(skip)
        .limit(limit)
        .order_by(Users.id)
    )
    users = result.scalars().all()

    count_result = await db.execute(select(func.count(Users.id)))
    total = count_result.scalar() or 0

    return {
        "items": [user for user in users],
        "total": total,
        "page": (skip // limit) + 1,
        "pages": max(1, (total + limit - 1) // limit),
        "limit": limit,
    }


# Update
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Users | None:
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


async def restore_user(db: AsyncSession, user_id: int) -> Users | None:
    result = await db.execute(
        select(Users)
        .where(Users.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    user.is_deleted = False
    await db.flush()
    await db.refresh(user)
    return user
