"""Генерация клиентской презентации в формате PPTX."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

from core.brand import load as load_brand
from core.config import OUTPUT_DIR
from core.exporter import office_to_pdf


def _hex_to_rgb(hex_color: str) -> RGBColor:
    """Преобразовать HEX-цвет в RGBColor для python-pptx."""
    hex_color = hex_color.lstrip("#")
    return RGBColor(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def _add_title_slide(prs: Presentation, brand: dict, client: str) -> None:
    """Титульный слайд."""
    slide_layout = prs.slide_layouts[6]  # пустой макет
    slide = prs.slides.add_slide(slide_layout)

    primary = _hex_to_rgb(brand["colors"]["primary"])
    text_color = _hex_to_rgb(brand["colors"]["text"])

    # Цветная полоса сверху
    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.4))
    shape.fill.solid()
    shape.fill.fore_color.rgb = primary
    shape.line.fill.background()

    title = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(8.6), Inches(1))
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = f"Презентация для {client}"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = primary

    subtitle = slide.shapes.add_textbox(Inches(0.7), Inches(2.7), Inches(8.6), Inches(1))
    tf = subtitle.text_frame
    p = tf.paragraphs[0]
    p.text = brand.get("company", "")
    p.font.size = Pt(24)
    p.font.color.rgb = text_color

    if brand.get("slogan"):
        slogan = slide.shapes.add_textbox(Inches(0.7), Inches(3.5), Inches(8.6), Inches(0.6))
        tf = slogan.text_frame
        p = tf.paragraphs[0]
        p.text = brand["slogan"]
        p.font.size = Pt(18)
        p.font.italic = True
        p.font.color.rgb = _hex_to_rgb(brand["colors"]["secondary"])


def _add_bullet_slide(prs: Presentation, brand: dict, title_text: str, bullets: list[str]) -> None:
    """Слайд с заголовком и списком."""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    primary = _hex_to_rgb(brand["colors"]["primary"])
    text_color = _hex_to_rgb(brand["colors"]["text"])

    # Полоса сверху
    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.25))
    shape.fill.solid()
    shape.fill.fore_color.rgb = primary
    shape.line.fill.background()

    title = slide.shapes.add_textbox(Inches(0.7), Inches(0.6), Inches(8.6), Inches(0.8))
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = primary

    body = slide.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(8.2), Inches(5))
    tf = body.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {bullet}"
        p.font.size = Pt(22)
        p.font.color.rgb = text_color
        p.space_after = Pt(14)


def _add_contacts_slide(prs: Presentation, brand: dict) -> None:
    """Финальный слайд с контактами."""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    primary = _hex_to_rgb(brand["colors"]["primary"])
    text_color = _hex_to_rgb(brand["colors"]["text"])

    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.25))
    shape.fill.solid()
    shape.fill.fore_color.rgb = primary
    shape.line.fill.background()

    title = slide.shapes.add_textbox(Inches(0.7), Inches(0.6), Inches(8.6), Inches(0.8))
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = "Контакты"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = primary

    contacts = brand.get("contacts", {})
    lines = [
        brand.get("company", ""),
        contacts.get("phone", ""),
        contacts.get("email", ""),
        contacts.get("site", ""),
        contacts.get("address", ""),
    ]

    body = slide.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(8.2), Inches(5))
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate([l for l in lines if l]):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(24)
        p.font.color.rgb = text_color
        p.space_after = Pt(12)


def generate(input_data: dict, output_dir: Path = OUTPUT_DIR, output_format: str = "pptx") -> Path:
    """Сгенерировать презентацию и вернуть путь к файлу.

    output_format: "pptx" или "pdf" (для PDF нужен LibreOffice)
    """
    brand = load_brand()
    output_dir.mkdir(parents=True, exist_ok=True)

    client_name = input_data.get("client_name", "Клиент")
    project_goal = input_data.get("project_goal", "")
    key_points = input_data.get("key_points", [])

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    _add_title_slide(prs, brand, client_name)

    if project_goal:
        _add_bullet_slide(prs, brand, "Цель проекта", [project_goal])

    if key_points:
        _add_bullet_slide(prs, brand, "Почему мы", key_points)

    _add_bullet_slide(prs, brand, "Следующие шаги", [
        "Согласование технического задания",
        "Подготовка коммерческого предложения",
        "Демонстрация решения",
    ])

    _add_contacts_slide(prs, brand)

    safe_name = client_name.replace(" ", "_").replace(".", "")
    pptx_path = output_dir / f"presentation_{safe_name}.pptx"
    prs.save(pptx_path)

    if output_format.lower() == "pdf":
        return office_to_pdf(pptx_path, output_dir)
    return pptx_path


if __name__ == "__main__":
    sample = {
        "client_name": "ООО РоторПром",
        "project_goal": "внедрение системы онлайн-вибродиагностики на мельничном оборудовании",
        "key_points": [
            "15 лет опыта в диагностике вращающегося оборудования",
            "более 200 успешных внедрений",
            "собственное производство датчиков",
            "техническая поддержка 24/7",
        ],
        "pages": 8,
    }
    path = generate(sample)
    print(f"Презентация сохранена: {path}")
