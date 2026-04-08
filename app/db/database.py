
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import get_db_cfg
db_cfg = get_db_cfg()


engine: AsyncEngine = create_async_engine(
	db_cfg.DB_URL,
	echo=db_cfg.DB_ECHO,
	pool_size=db_cfg.DB_POOL_SIZE,
	max_overflow=db_cfg.DB_MAX_OVERFLOW,
	pool_recycle=db_cfg.DB_POOL_RECYCLE,
)

async_session_factory = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autoflush=False,
)

