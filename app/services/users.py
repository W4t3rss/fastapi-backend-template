
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users import get_user_by_user_name
from app.models.users import Users
from app.schemas.users import (UserCreate,UserCreateAdmin,)
from app.crud import * 
from app.exceptions import *
from app.core.security import create_password_hash
from app.utils import logger


async def create_user(db: AsyncSession, user_create: UserCreate) -> Users:
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
    except (UsernameAlreadyExistsException, PhoneAlreadyExistsException):
        await db.rollback()
        raise 
    except Exception as e:
        await db.rollback()
        raise