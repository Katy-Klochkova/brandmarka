"""Минимальные тесты для генераторов Brandmarka.

Проверяем, что каждый генератор отрабатывает без ошибок
и создаёт непустой файл на demo-данных.
"""

import json
import sys
from pathlib import Path

import pytest

# Добавляем src в путь при запуске тестов
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from core.config import OUTPUT_DIR  # noqa: E402
from generators.business_card import generate as generate_business_card  # noqa: E402
from generators.email_signature import generate as generate_email_signature  # noqa: E402
from generators.presentation import generate as generate_presentation  # noqa: E402
from generators.proposal import generate as generate_proposal  # noqa: E402


def _load_sample(name: str) -> dict:
    path = PROJECT_DIR / "demo" / "sample-inputs" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def test_business_card_generates_png(output_dir: Path) -> None:
    data = _load_sample("employee")
    path = generate_business_card(data, output_dir=output_dir, output_format="png")
    assert path.exists()
    assert path.stat().st_size > 0


def test_email_signature_generates_html(output_dir: Path) -> None:
    data = _load_sample("employee")
    path = generate_email_signature(data, output_dir=output_dir)
    assert path.exists()
    assert path.stat().st_size > 0
    html = path.read_text(encoding="utf-8")
    assert "<table" in html


def test_presentation_generates_pptx(output_dir: Path) -> None:
    data = _load_sample("client")
    path = generate_presentation(data, output_dir=output_dir, output_format="pptx")
    assert path.exists()
    assert path.stat().st_size > 0


def test_proposal_generates_docx(output_dir: Path) -> None:
    data = _load_sample("proposal")
    path = generate_proposal(data, output_dir=output_dir, output_format="docx")
    assert path.exists()
    assert path.stat().st_size > 0
