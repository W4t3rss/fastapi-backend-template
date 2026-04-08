
from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.models.users import Users
from app.schemas.users import UserRead, UserUpdate
from app.services.users import update_user_service
user_router = APIRouter()


# app/api/v1/users/me
@user_router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
)
async def get_me(
    current_user: Users = Depends(get_current_user),
) -> UserRead:
    return UserRead.model_validate(current_user)


# app/api/v1/users/me
@user_router.patch(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
)
async def update_me(
    user_update: Annotated[
        UserUpdate,
        Body(
            openapi_examples={
                "full_update": {
                    "summary": "Complete example",
                    "value": {
                        "user_name": "user1_new",
                        "phone_number": "13800138001",
                        "password": "87654321",
                    },
                },
                "rename_profile": {
                    "summary": "Change username",
                    "value": {
                        "user_name": "user1_new",
                    },
                },
                "change_phone": {
                    "summary": "Change phone number",
                    "value": {
                        "phone_number": "13800138001",
                    },
                },
                "change_password": {
                    "summary": "Change password",
                    "value": {
                        "password": "87654321",
                    },
                },
            }
        ),
    ],
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user),
) -> UserRead:
    user = await update_user_service(db, current_user.id, user_update)
    return UserRead.model_validate(user)
