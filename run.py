"""Точка входа для запуска Brandmarka из корня проекта."""

import sys
from pathlib import Path

# Добавляем папку src в пути импортов, чтобы модули core, generators и api находились
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "src"))

from cli.brandmarka import main

if __name__ == "__main__":
    main()
