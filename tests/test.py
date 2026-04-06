
from app.core.config import get_path_cfg
path_cfg = get_path_cfg()


if __name__ == "__main__":
    print(path_cfg.PROJECT_ROOT)