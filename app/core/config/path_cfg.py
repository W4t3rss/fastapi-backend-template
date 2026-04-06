
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PathConfig:

    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent.parent  # E:\Code\fastapi-backend