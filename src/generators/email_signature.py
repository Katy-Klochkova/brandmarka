"""Генерация HTML email-подписи."""

from pathlib import Path

from core.brand import load as load_brand
from core.config import OUTPUT_DIR


def generate(input_data: dict, output_dir: Path = OUTPUT_DIR) -> Path:
    """Сгенерировать HTML email-подпись и вернуть путь к файлу."""
    brand = load_brand()
    output_dir.mkdir(parents=True, exist_ok=True)

    full_name = input_data.get("full_name", "")
    position = input_data.get("position", "")
    phone = input_data.get("phone", "")
    email = input_data.get("email", "")
    telegram = input_data.get("telegram", "")

    company = brand.get("company", "")
    slogan = brand.get("slogan", "")
    contacts = brand.get("contacts", {})

    primary = brand.get("colors", {}).get("primary", "#003366")
    secondary = brand.get("colors", {}).get("secondary", "#00A3E0")
    text_color = brand.get("colors", {}).get("text", "#1A1A1A")

    site = contacts.get("site", "")
    company_phone = contacts.get("phone", "")
    company_email = contacts.get("email", "")

    telegram_link = f'| <a href="https://t.me/{telegram.lstrip("@")}" style="color:{secondary};text-decoration:none;">{telegram}</a>' if telegram else ""

    html = f"""
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,sans-serif;font-size:14px;color:{text_color};">
  <tr>
    <td style="padding-right:16px;border-right:2px solid {primary};">
      <div style="font-size:18px;font-weight:bold;color:{primary};">{full_name}</div>
      <div style="color:{secondary};">{position}</div>
    </td>
    <td style="padding-left:16px;">
      <div style="font-weight:bold;color:{primary};">{company}</div>
      <div>{phone}</div>
      <div><a href="mailto:{email}" style="color:{secondary};text-decoration:none;">{email}</a></div>
      <div>{site} {telegram_link}</div>
      {f'<div style="margin-top:4px;font-size:12px;color:#666;">{slogan}</div>' if slogan else ""}
    </td>
  </tr>
</table>
"""

    safe_name = full_name.replace(" ", "_").replace(".", "")
    out_path = output_dir / f"email_signature_{safe_name}.html"
    out_path.write_text(html.strip(), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    sample = {
        "full_name": "Иванов Иван Иванович",
        "position": "Руководитель отдела продаж",
        "phone": "+7 900 123-45-67",
        "email": "ivanov@techdiagnostika.ru",
        "telegram": "@ivanov_td",
    }
    path = generate(sample)
    print(f"Подпись сохранена: {path}")
