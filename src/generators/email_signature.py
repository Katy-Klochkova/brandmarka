"""Генерация HTML email-подписи в стиле Anthropic."""

import base64
from pathlib import Path

from core.brand import load as load_brand
from core.config import BASE_DIR, OUTPUT_DIR


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

    # Антропик-стиль по умолчанию
    primary = brand.get("colors", {}).get("primary", "#1F1F1E")
    secondary = brand.get("colors", {}).get("secondary", "#5A4BFF")
    accent = brand.get("colors", {}).get("accent", "#FF5B24")
    text_color = brand.get("colors", {}).get("text", "#1F1F1E")

    site = contacts.get("site", "")

    logo_url = brand.get("logo_url", "")
    logo_html = ""
    if logo_url:
        try:
            logo_path = BASE_DIR / logo_url.lstrip("/")
            if logo_path.exists():
                ext = logo_path.suffix.lower()
                mime = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".svg": "image/svg+xml",
                }.get(ext, "image/png")
                b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
                logo_html = (
                    f'<td valign="top" style="padding-left:16px;">'
                    f'<img src="data:{mime};base64,{b64}" alt="{company}" '
                    f'style="max-height:54px; width:auto; display:block;">'
                    f'</td>'
                )
        except Exception:
            logo_html = ""

    telegram_html = (
        f'<span style="margin-left:8px;">'
        f'<a href="https://t.me/{telegram.lstrip("@")}" '
        f'style="color:{secondary};text-decoration:none;font-weight:500;">{telegram}</a>'
        f'</span>'
        if telegram else ""
    )

    site_html = (
        f'<a href="https://{site}" style="color:{secondary};text-decoration:none;font-weight:500;">{site}</a>'
        if site else ""
    )

    html = f"""
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Inter, Arial, sans-serif; font-size:14px; color:{text_color}; line-height:1.6;">
  <tr>
    <td style="width:6px; background:{secondary}; border-radius:3px;"></td>
    <td style="width:10px;"></td>
    <td style="padding:4px 0;">
      <div style="font-size:17px; font-weight:600; color:{primary}; letter-spacing:-0.01em;">{full_name}</div>
      <div style="color:{secondary}; font-weight:500; margin-top:1px;">{position} · {company}</div>
      <div style="margin-top:10px;">
        <span>{phone}</span>
        <span style="margin:0 8px; color:{accent};">·</span>
        <a href="mailto:{email}" style="color:{secondary}; text-decoration:none; font-weight:500;">{email}</a>
      </div>
      <div style="margin-top:2px;">
        {site_html}
        {telegram_html}
      </div>
      {f'<div style="margin-top:10px; font-size:12px; color:#6B6B6A; font-style:italic;">{slogan}</div>' if slogan else ""}
    </td>
    {logo_html}
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
