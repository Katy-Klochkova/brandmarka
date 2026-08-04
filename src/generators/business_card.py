"""Генерация визитки сотрудника."""

import io
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

from core.brand import load as load_brand
from core.config import OUTPUT_DIR

# Размер визитки: 90×50 мм при 300 dpi = 1063×591 px
WIDTH = 1063
HEIGHT = 591
MARGIN = 60


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Подобрать шрифт из системы."""
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    # Фолбэк на стандартный шрифт Pillow
    return ImageFont.load_default()


def _text_size(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Вернуть ширину и высоту текста."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _wrap_text(
    draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    """Разбить текст на строки, чтобы каждая укладывалась в max_width."""
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = words[0]
    for word in words[1:]:
        test_line = f"{current_line} {word}"
        w, _ = _text_size(draw, test_line, font)
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines


def _make_qr_vcard(data: dict, brand: dict) -> Image.Image:
    """Создать QR-код с vCard."""
    phone = data.get("phone", "").replace(" ", "").replace("-", "")
    email = data.get("email", "")
    full_name = data.get("full_name", "")
    position = data.get("position", "")
    company = brand.get("company", "")

    vcard = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{full_name}\n"
        f"ORG:{company}\n"
        f"TITLE:{position}\n"
        f"TEL;TYPE=CELL:{phone}\n"
        f"EMAIL:{email}\n"
        "END:VCARD"
    )

    qr = qrcode.make(vcard, box_size=6, border=2)
    return qr.convert("RGB")


def generate(input_data: dict, output_dir: Path = OUTPUT_DIR) -> Path:
    """Сгенерировать PNG-визитку и вернуть путь к файлу."""
    brand = load_brand()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Цвета из бренд-бука
    primary = brand.get("colors", {}).get("primary", "#003366")
    background = brand.get("colors", {}).get("background", "#FFFFFF")
    text_color = brand.get("colors", {}).get("text", "#1A1A1A")
    secondary = brand.get("colors", {}).get("secondary", "#00A3E0")

    # Создаём холст
    img = Image.new("RGB", (WIDTH, HEIGHT), background)
    draw = ImageDraw.Draw(img)

    # Рамка сверху в цвет бренда
    draw.rectangle([(0, 0), (WIDTH, 12)], fill=primary)

    # Шрифты
    font_name = _get_font(54, bold=True)
    font_position = _get_font(32)
    font_contact = _get_font(26)
    font_company = _get_font(28, bold=True)
    font_slogan = _get_font(20)

    # Текст
    full_name = input_data.get("full_name", "")
    position = input_data.get("position", "")
    phone = input_data.get("phone", "")
    email = input_data.get("email", "")
    telegram = input_data.get("telegram", "")
    company = brand.get("company", "")
    slogan = brand.get("slogan", "")

    # Разделяем визитку на две колонки
    left_x = MARGIN
    left_w = int(WIDTH * 0.52) - MARGIN
    right_x = int(WIDTH * 0.56)
    right_w = WIDTH - right_x - MARGIN

    # Левая колонка: ФИО и должность с переносом
    y = 70
    name_lines = _wrap_text(draw, full_name, font_name, left_w)
    for line in name_lines:
        draw.text((left_x, y), line, fill=text_color, font=font_name)
        _, h = _text_size(draw, line, font_name)
        y += h + 10

    position_lines = _wrap_text(draw, position, font_position, left_w)
    for line in position_lines:
        draw.text((left_x, y), line, fill=secondary, font=font_position)
        _, h = _text_size(draw, line, font_position)
        y += h + 8
    y += 30

    # Контакты
    contacts = []
    if phone:
        contacts.append(f"{phone}")
    if email:
        contacts.append(f"{email}")
    if telegram:
        contacts.append(f"Telegram: {telegram}")

    for line in contacts:
        draw.text((left_x, y), line, fill=text_color, font=font_contact)
        y += 44

    # Правая колонка: компания, слоган, QR
    company_lines = _wrap_text(draw, company, font_company, right_w)
    cy = 70
    for line in company_lines:
        draw.text((right_x, cy), line, fill=primary, font=font_company)
        _, h = _text_size(draw, line, font_company)
        cy += h + 6

    if slogan:
        cy += 10
        slogan_lines = _wrap_text(draw, slogan, font_slogan, right_w)
        for line in slogan_lines:
            draw.text((right_x, cy), line, fill=text_color, font=font_slogan)
            _, h = _text_size(draw, line, font_slogan)
            cy += h + 4

    # QR-код vCard в правом нижнем углу
    qr = _make_qr_vcard(input_data, brand)
    qr_size = 170
    qr = qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qr_x = WIDTH - MARGIN - qr_size
    qr_y = HEIGHT - MARGIN - qr_size
    img.paste(qr, (qr_x, qr_y))

    # Сохраняем
    safe_name = full_name.replace(" ", "_").replace(".", "")
    out_path = output_dir / f"business_card_{safe_name}.png"
    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    # Тестовый запуск
    sample = {
        "full_name": "Иванов Иван Иванович",
        "position": "Руководитель отдела продаж",
        "phone": "+7 900 123-45-67",
        "email": "ivanov@techdiagnostika.ru",
        "telegram": "@ivanov_td",
    }
    path = generate(sample)
    print(f"Визитка сохранена: {path}")
