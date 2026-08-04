"""Работа с бренд-буком компании."""

import json

from core.config import DATA_DIR

BRAND_PATH = DATA_DIR / "brandbook.json"


def load() -> dict:
    """Загрузить бренд-бук из файла."""
    if not BRAND_PATH.exists():
        raise FileNotFoundError("Бренд-бук не найден. Сначала загрузите brandbook.json")
    return json.loads(BRAND_PATH.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    """Сохранить бренд-бук."""
    BRAND_PATH.parent.mkdir(parents=True, exist_ok=True)
    BRAND_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def validate(data: dict) -> list[str]:
    """Проверить обязательные поля бренд-бука."""
    required = ["company", "colors", "fonts", "contacts"]
    return [f"Отсутствует поле: {key}" for key in required if key not in data]
