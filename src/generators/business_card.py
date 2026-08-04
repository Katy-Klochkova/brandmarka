"""Генерация визитки."""

from pathlib import Path

from core.brand import load as load_brand


def generate(input_data: dict, output_dir: Path = Path("output")) -> Path:
    """Сгенерировать PNG-визитку и вернуть путь к файлу."""
    brand = load_brand()
    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: интеграция с LLM и рендерером
    out_path = output_dir / f"business_card_{input_data['full_name'].replace(' ', '_')}.png"
    out_path.write_text("placeholder", encoding="utf-8")
    return out_path
