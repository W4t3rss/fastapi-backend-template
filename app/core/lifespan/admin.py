
from sqlalchemy import select
from app.core.config import get_db_cfg
from app.core.security import create_password_hash
from app.db.database import async_session_factory
from app.models.users import Users
from .logger import logger
db_cfg = get_db_cfg()


async def init_admin_user() -> None:
	admin_name = db_cfg.INIT_ADMIN.strip()
	admin_password = db_cfg.INIT_ADMIN_PASSWORD

	if not admin_name:
		logger.warning("Skip admin initialization: INIT_ADMIN is empty")
		return

	if not admin_password:
		logger.warning("Skip admin initialization: INIT_ADMIN_PASSWORD is empty")
		return

	async with async_session_factory() as session:
		try:
			result = await session.execute(
				select(Users).where(Users.user_name == admin_name)
			)
			user = result.scalar_one_or_none()

			if user is None:
				admin = Users(
					role=1,
					user_name=admin_name,
					password=create_password_hash(admin_password),
					phone_number=None,
				)
				session.add(admin)
				await session.commit()
				logger.info("Admin account initialized: user_name={}", admin_name)
				return

			updated = False
			if user.role != 1:
				user.role = 1
				updated = True
			if user.is_deleted:
				user.is_deleted = False
				updated = True

			if updated:
				await session.commit()
				logger.info("Existing account promoted to admin: user_name={}", admin_name)
			else:
				logger.info("Admin account already exists: user_name={}", admin_name)

		except Exception as e:
			await session.rollback()
			logger.exception("Failed to initialize admin account: {}", e)
			raise
