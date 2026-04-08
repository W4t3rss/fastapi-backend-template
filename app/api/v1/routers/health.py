
from fastapi import APIRouter
from app.core.config import get_app_cfg
app_cfg = get_app_cfg()
health_router = APIRouter()


# /health
@health_router.get("/health", tags=["system"], summary="Health check")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": app_cfg.APP_NAME,
        "version": app_cfg.APP_VERSION,
    }
