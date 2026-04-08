from .admin import admini_router
from .auth import auth_router
from .health import health_router
from .pets import pets_router
from .users import user_router


__all__ = [
    "admini_router",
    "auth_router",
    "health_router",
    "pets_router",
    "user_router",
]
