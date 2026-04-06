
from dataclasses import dataclass
from pathlib import Path
from functools import lru_cache


@dataclass
class PathCfg:

    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent.parent
    LOGS_PATH: Path = PROJECT_ROOT / "app" / "logs"


@lru_cache
def get_path_cfg() -> PathCfg:
    return PathCfg()