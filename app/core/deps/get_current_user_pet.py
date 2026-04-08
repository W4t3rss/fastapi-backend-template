from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.base import ForbiddenException
from app.models.pets import Pets
from app.models.users import Users
from app.services.pets import get_pet_by_id_service
from .get_current_user import get_current_user
from .get_db import get_db


async def get_current_user_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> Pets:
    pet = await get_pet_by_id_service(db, pet_id)
    if pet.owner_id != current_user.id:
        raise ForbiddenException(message="You do not have permission to access this pet")
    return pet