

from app.api.v1.routers import pets_router, user_router, auth_router, admini_router
from fastapi import FastAPI


v1_router = FastAPI()
v1_router.include_router(pets_router, prefix="/pets", tags=["pets"])
v1_router.include_router(user_router, prefix="/users", tags=["users"])
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(admini_router, prefix="/admin", tags=["admin"])
