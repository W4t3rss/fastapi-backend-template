
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import Users
from app.schemas.users import (UserCreate,UserCreateAdmin,
                               UserRead, UserReadAdmin, 
                               UserUpdate, UserUpdateAdmin
                               )
from app.core.security import hash_password 
from sqlalchemy import func, select
from app.core.config.db_cfg import get_db_cfg
db_cfg = get_db_cfg()


# Create
async def create_user(db: AsyncSession, user_create: UserCreate) -> UserRead:
    user = Users(
        user_name=user_create.user_name,
        phone_number=user_create.phone_number,
        password=hash_password(user_create.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserRead.model_validate(user)

async def create_user_admin(db: AsyncSession, user_create: UserCreateAdmin) -> UserReadAdmin:
    user = Users(
        role=user_create.role,
        user_name=user_create.user_name,
        phone_number=user_create.phone_number,
        password=hash_password(user_create.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserReadAdmin.model_validate(user)


# Read
async def get_user_by_id(db: AsyncSession, user_id: int) -> UserReadAdmin | None:
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
    return UserReadAdmin.model_validate(user)


async def get_all_users(db: AsyncSession) -> dict:
    skip = db_cfg.SKIP
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
        "items": [UserReadAdmin.model_validate(user) for user in users],
        "total": total,
        "page": (skip // limit) + 1,
        "pages": (total + limit - 1) // limit,
        "size": limit   
    }


# Update
async def update_user(db: AsyncSession, user_update: UserUpdate) -> UserRead | None:
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_update.id, 
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
        user.password = hash_password(user_update.password)

    await db.commit()
    await db.refresh(user)
    return UserRead.model_validate(user)

async def update_user_admin(db: AsyncSession, user_update: UserUpdateAdmin) -> UserReadAdmin | None:
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_update.id, 
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
        user.password = hash_password(user_update.password)
    if user_update.role is not None:
        user.role = user_update.role

    await db.commit()
    await db.refresh(user)
    return UserReadAdmin.model_validate(user)


# Delete
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(
        select(Users)
        .where(
            Users.id == user_id, 
            Users.is_deleted == False
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        return False

    user.is_deleted = True
    await db.commit()
    return True
