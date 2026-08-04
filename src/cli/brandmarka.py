"""Консольная утилита Brandmarka."""

import argparse
import json
from pathlib import Path

from core.brand import save as save_brand
from generators import business_card, email_signature, presentation, proposal


def main():
    parser = argparse.ArgumentParser(description="Brandmarka CLI")
    sub = parser.add_subparsers(dest="command")

    upload = sub.add_parser("upload-brandbook", help="Загрузить бренд-бук")
    upload.add_argument("--file", required=True, help="Путь к brandbook.json")
    upload.add_argument("--logo", help="Путь к файлу логотипа (PNG, JPG, SVG)")

    card = sub.add_parser("business-card", help="Сгенерировать визитку")
    card.add_argument("--input", required=True, help="Путь к JSON с данными сотрудника")
    card.add_argument("--format", choices=["png", "pdf"], default="png", help="Формат выходного файла")

    sign = sub.add_parser("email-signature", help="Сгенерировать email-подпись")
    sign.add_argument("--input", required=True, help="Путь к JSON с данными сотрудника")

    pres = sub.add_parser("presentation", help="Сгенерировать презентацию")
    pres.add_argument("--input", required=True, help="Путь к JSON с данными клиента")
    pres.add_argument("--format", choices=["pptx", "pdf"], default="pptx", help="Формат выходного файла")

    prop = sub.add_parser("proposal", help="Сгенерировать КП")
    prop.add_argument("--input", required=True, help="Путь к JSON с данными клиента")
    prop.add_argument("--format", choices=["docx", "pdf"], default="docx", help="Формат выходного файла")

    args = parser.parse_args()

    if args.command == "upload-brandbook":
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
        if args.logo:
            from core.config import UPLOADS_DIR
            logo_path = Path(args.logo)
            if not logo_path.exists():
                print(f"Логотип не найден: {logo_path}")
                return
            ext = logo_path.suffix.lower()
            if ext not in {".png", ".jpg", ".jpeg", ".svg"}:
                print("Логотип должен быть PNG, JPG или SVG")
                return
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            target = UPLOADS_DIR / f"logo{ext}"
            target.write_bytes(logo_path.read_bytes())
            data["logo_url"] = f"/uploads/logo{ext}"
            print(f"Логотип загружен: {target}")
        save_brand(data)
        print("Бренд-бук загружен.")
    elif args.command == "business-card":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = business_card.generate(inp, output_format=args.format)
        print(f"Визитка сохранена: {path}")
    elif args.command == "email-signature":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = email_signature.generate(inp)
        print(f"Email-подпись сохранена: {path}")
    elif args.command == "presentation":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = presentation.generate(inp, output_format=args.format)
        print(f"Презентация сохранена: {path}")
    elif args.command == "proposal":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = proposal.generate(inp, output_format=args.format)
        print(f"КП сохранено: {path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
