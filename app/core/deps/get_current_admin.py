
from fastapi import Depends
from app.core.deps.get_current_user import get_current_user
from app.exceptions.base import ForbiddenException
from app.models.users import Users


async def get_current_admin(
    current_user: Users = Depends(get_current_user),
) -> Users:
    if current_user.role != 1:
        raise ForbiddenException(message="Admin permission required")
    return current_user