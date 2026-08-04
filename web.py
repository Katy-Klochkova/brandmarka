"""Запуск веб-сервера Brandmarka."""

import sys
from pathlib import Path

# Добавляем src в пути импортов
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "src"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.routes:app", host="127.0.0.1", port=8000, reload=True)
