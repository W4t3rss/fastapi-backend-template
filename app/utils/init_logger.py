
import sys
import os
from pathlib import Path
from loguru import logger
from app.core.config import path_cfg
from app.core.config.path_cfg import get_path_cfg   
path_cfg = get_path_cfg()


def init_logger(level: str | None = None) -> None:
    """
    初始化日志系统，配置终端和文件日志
    :param level: 可选的日志级别，默认为环境变量 LOG_LEVEL 或 "DEBUG"。
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "DEBUG").upper()
    logger.remove()

    # 终端
    logger.add(
        sys.stdout,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True,     
        enqueue=True,       
    )

    # 文件
    log_path = path_cfg.LOGS_PATH
    log_path.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_path / "{time:YYYY-MM-DD}.log",   # 每天一个文件
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="00:00",      # 每天凌晨 0 点切割
        retention="30 days",   # 自动保留最近 30 天
        compression="zip",     # 压缩旧日志节省空间
        encoding="utf-8",
        enqueue=True,
    )

