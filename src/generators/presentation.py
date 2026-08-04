"""Генерация клиентской презентации."""

from pathlib import Path

from core.brand import load as load_brand


def generate(input_data: dict, output_dir: Path = Path("output")) -> Path:
    """Сгенерировать PPTX-презентацию и вернуть путь к файлу."""
    brand = load_brand()
    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: интеграция с LLM и python-pptx
    out_path = output_dir / f"presentation_{input_data['client_name'].replace(' ', '_')}.pptx"
    out_path.write_text("placeholder", encoding="utf-8")
    return out_path
