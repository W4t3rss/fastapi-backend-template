
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.models import Base
from app.core.config import get_db_cfg


config = context.config
db_cfg = get_db_cfg()
config.set_main_option("sqlalchemy.url", db_cfg.DB_URL)
target_metadata = Base.metadata 

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """
    离线模式：
    不真正连接数据库，只根据 URL 生成 SQL / 执行迁移上下文。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,            # 检测字段类型变化
        compare_server_default=True,  # 检测 server_default 变化
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    真正执行迁移的同步部分。
    Alembic 的迁移上下文仍然是同步配置方式，
    即使外层用的是异步 engine。
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,            # 检测字段类型变化
        compare_server_default=True,  # 检测 server_default 变化
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    在线模式：
    使用异步 engine 连接数据库，再交给 Alembic 执行迁移。
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()