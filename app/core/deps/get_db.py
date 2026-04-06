
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
	"""
    创建一个新的数据库会话，并在请求结束后自动关闭它，确保资源得到正确释放
	:return: 一个异步生成器
    """
	async with async_session_factory() as session:
		yield session