"""Утилиты для работы с логотипами."""

from pathlib import Path
from typing import Optional

from PIL import Image


def _svg_to_png(svg_path: Path, png_path: Path, width: int = 400) -> None:
    """Конвертировать SVG в PNG через svglib + reportlab."""
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM

    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise ValueError(f"Не удалось распарсить SVG: {svg_path}")
    # Масштабируем под нужную ширину
    scale = width / drawing.width
    drawing.width = width
    drawing.height = drawing.height * scale
    drawing.scale(scale, scale)
    renderPM.drawToFile(drawing, str(png_path), fmt="PNG")


def prepare_logo(logo_url: str, base_dir: Path, width: int = 400) -> Optional[Path]:
    """Вернуть путь к PNG-версии логотипа, при необходимости сконвертировав SVG.

    Для PNG/JPG возвращает исходный файл.
    Для SVG создаёт временный PNG в той же папке.
    Если логотип не найден или формат не поддерживается — возвращает None.
    """
    if not logo_url:
        return None

    logo_path = base_dir / logo_url.lstrip("/")
    if not logo_path.exists():
        return None

    ext = logo_path.suffix.lower()
    if ext in {".png", ".jpg", ".jpeg"}:
        return logo_path

    if ext == ".svg":
        try:
            png_path = logo_path.with_suffix(".png")
            _svg_to_png(logo_path, png_path, width=width)
            return png_path
        except Exception:
            return None

    return None


def open_logo(logo_url: str, base_dir: Path, width: int = 400) -> Optional[Image.Image]:
    """Открыть логотип как PIL Image, конвертируя SVG при необходимости."""
    path = prepare_logo(logo_url, base_dir, width=width)
    if path is None:
        return None
    try:
        return Image.open(path).convert("RGBA")
    except Exception:
        return None
