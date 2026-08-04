"""Консольная утилита Brandmarka."""

import argparse
import json
from pathlib import Path

from core.brand import save as save_brand
from generators import business_card, presentation, proposal


def main():
    parser = argparse.ArgumentParser(description="Brandmarka CLI")
    sub = parser.add_subparsers(dest="command")

    upload = sub.add_parser("upload-brandbook", help="Загрузить бренд-бук")
    upload.add_argument("--file", required=True, help="Путь к brandbook.json")

    card = sub.add_parser("business-card", help="Сгенерировать визитку")
    card.add_argument("--input", required=True, help="Путь к JSON с данными сотрудника")

    pres = sub.add_parser("presentation", help="Сгенерировать презентацию")
    pres.add_argument("--input", required=True, help="Путь к JSON с данными клиента")

    prop = sub.add_parser("proposal", help="Сгенерировать КП")
    prop.add_argument("--input", required=True, help="Путь к JSON с данными клиента")

    args = parser.parse_args()

    if args.command == "upload-brandbook":
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
        save_brand(data)
        print("Бренд-бук загружен.")
    elif args.command == "business-card":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = business_card.generate(inp)
        print(f"Визитка сохранена: {path}")
    elif args.command == "presentation":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = presentation.generate(inp)
        print(f"Презентация сохранена: {path}")
    elif args.command == "proposal":
        inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
        path = proposal.generate(inp)
        print(f"КП сохранено: {path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
