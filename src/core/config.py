"""Настройки проекта из переменных окружения."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные из .env, если он есть
load_dotenv()

# Базовая папка проекта — на два уровня выше от src/core/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Папки для данных и результатов
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
UPLOADS_DIR = BASE_DIR / "uploads"

for folder in (DATA_DIR, OUTPUT_DIR, UPLOADS_DIR):
    folder.mkdir(parents=True, exist_ok=True)

# API-ключ Claude (нужен только для LLM-генераторов)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
