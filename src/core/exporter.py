"""Экспорт сгенерированных файлов в PDF."""

import shutil
import subprocess
from pathlib import Path

from PIL import Image


def png_to_pdf(png_path: Path, pdf_path: Path | None = None) -> Path:
    """Конвертировать PNG-изображение в PDF."""
    png_path = Path(png_path)
    if pdf_path is None:
        pdf_path = png_path.with_suffix(".pdf")
    else:
        pdf_path = Path(pdf_path)

    img = Image.open(png_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(pdf_path, "PDF", resolution=300.0)
    return pdf_path


def _find_libreoffice() -> str | None:
    """Найти исполняемый файл LibreOffice (soffice/libreoffice)."""
    for cmd in ("soffice", "libreoffice"):
        if shutil.which(cmd):
            return cmd
    return None


def office_to_pdf(source_path: Path, output_dir: Path | None = None) -> Path:
    """Конвертировать DOCX/PPTX в PDF через LibreOffice.

    Возвращает путь к PDF-файлу.
    Выбрасывает RuntimeError, если LibreOffice не найден.
    """
    source_path = Path(source_path)
    if output_dir is None:
        output_dir = source_path.parent
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    libreoffice = _find_libreoffice()
    if not libreoffice:
        raise RuntimeError(
            "LibreOffice не найден. Установите LibreOffice для конвертации в PDF:\n"
            "https://www.libreoffice.org/download/download/"
        )

    cmd = [
        libreoffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(source_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pdf_name = source_path.stem + ".pdf"
    pdf_path = output_dir / pdf_name
    if not pdf_path.exists():
        raise RuntimeError(f"Не удалось создать PDF: {pdf_path}")
    return pdf_path
