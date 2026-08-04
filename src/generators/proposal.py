"""Генерация коммерческого предложения в формате DOCX."""

from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from core.brand import load as load_brand
from core.config import OUTPUT_DIR
from core.exporter import office_to_pdf


def _hex_to_rgb(hex_color: str) -> RGBColor:
    """Преобразовать HEX в RGBColor."""
    hex_color = hex_color.lstrip("#")
    return RGBColor(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def generate(input_data: dict, output_dir: Path = OUTPUT_DIR, output_format: str = "docx") -> Path:
    """Сгенерировать коммерческое предложение и вернуть путь к файлу.

    output_format: "docx" или "pdf" (для PDF нужен LibreOffice)
    """
    brand = load_brand()
    output_dir.mkdir(parents=True, exist_ok=True)

    client_name = input_data.get("client_name", "")
    services = input_data.get("services", [])
    terms = input_data.get("terms", "")
    payment = input_data.get("payment", "")
    company = brand.get("company", "")
    slogan = brand.get("slogan", "")
    contacts = brand.get("contacts", {})

    primary = _hex_to_rgb(brand["colors"]["primary"])
    text_color = _hex_to_rgb(brand["colors"]["text"])

    doc = Document()

    # Заголовок
    title = doc.add_heading(f"Коммерческое предложение", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.color.rgb = primary
        run.font.size = Pt(22)
        run.font.bold = True

    # Кому
    p = doc.add_paragraph()
    p.add_run(f"Для: {client_name}").bold = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # От кого
    p = doc.add_paragraph()
    p.add_run(f"От: {company}").bold = True
    if slogan:
        p.add_run(f"\n{slogan}")

    doc.add_paragraph()

    # Введение
    intro = doc.add_paragraph()
    intro.add_run(
        f"{company} предлагает выполнить работы для {client_name} в соответствии с нижеуказанным перечнем услуг и условиями."
    )

    doc.add_paragraph()

    # Таблица услуг
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "№"
    hdr_cells[1].text = "Услуга"
    hdr_cells[2].text = "Стоимость, руб."

    total = 0
    for i, service in enumerate(services, start=1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(i)
        row_cells[1].text = service.get("name", "")
        price = service.get("price", 0)
        row_cells[2].text = f"{price:,.0f}".replace(",", " ")
        total += price

    # Итого
    row_cells = table.add_row().cells
    row_cells[0].text = ""
    row_cells[1].text = "Итого"
    row_cells[2].text = f"{total:,.0f}".replace(",", " ")
    for run in row_cells[1].paragraphs[0].runs:
        run.bold = True
    for run in row_cells[2].paragraphs[0].runs:
        run.bold = True

    doc.add_paragraph()

    # Сроки и оплата
    if terms:
        p = doc.add_paragraph()
        p.add_run("Сроки выполнения: ").bold = True
        p.add_run(terms)

    if payment:
        p = doc.add_paragraph()
        p.add_run("Условия оплаты: ").bold = True
        p.add_run(payment)

    doc.add_paragraph()

    # Контакты
    p = doc.add_paragraph()
    p.add_run("Контакты для связи:\n").bold = True
    contact_lines = [
        contacts.get("phone", ""),
        contacts.get("email", ""),
        contacts.get("site", ""),
    ]
    p.add_run("\n".join([l for l in contact_lines if l]))

    safe_name = client_name.replace(" ", "_").replace(".", "")
    docx_path = output_dir / f"proposal_{safe_name}.docx"
    doc.save(docx_path)

    if output_format.lower() == "pdf":
        return office_to_pdf(docx_path, output_dir)
    return docx_path


if __name__ == "__main__":
    sample = {
        "client_name": "ООО РоторПром",
        "services": [
            {"name": "Поставка системы вибродиагностики", "price": 1250000},
            {"name": "Монтаж и пусконаладка", "price": 280000},
            {"name": "Обучение персонала", "price": 120000},
        ],
        "terms": "30 рабочих дней с момента подписания договора",
        "payment": "50% предоплата, 50% после ввода в эксплуатацию",
    }
    path = generate(sample)
    print(f"КП сохранено: {path}")
