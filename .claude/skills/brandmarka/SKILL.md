---
name: brandmarka
description: Работа с репозиторием Brandmarka — понимать структуру, запускать сервис, вносить изменения, проверять ошибки, обновлять README и готовить проект к публикации.
---

# Brandmarka

Генератор фирменных маркетинговых материалов в едином бренд-стиле. Стек: Python 3.12+, FastAPI, Pillow, python-pptx, python-docx, qrcode.

## Быстрый старт

Windows:

```bash
cd C:\Users\Admin\myai\NPP_IT\итоговый проект\brandmarka
.venv\Scripts\activate
pip install -r requirements.txt
python web.py
```

Открыть в браузере: `http://127.0.0.1:8000`

CLI:

```bash
python run.py --help
python run.py business-card --input demo/sample-inputs/employee.json
```

## Ключевая структура

- `web.py` — запуск веб-сервера (Uvicorn + reload).
- `run.py` — точка входа для CLI.
- `requirements.txt` — зависимости Python.
- `src/api/routes.py` — FastAPI эндпоинты и раздача статики.
- `src/core/`
  - `brand.py` — загрузка/сохранение `data/brandbook.json`.
  - `config.py` — пути (`BASE_DIR`, `DATA_DIR`, `OUTPUT_DIR`, `UPLOADS_DIR`) и `ANTHROPIC_API_KEY`.
  - `images.py` — работа с логотипами PNG/JPG/SVG.
  - `exporter.py` — конвертация PNG → PDF и DOCX/PPTX → PDF через LibreOffice.
  - `llm.py` — подключение Claude API (подготовлено, не обязательно для MVP).
- `src/generators/`
  - `business_card.py` — визитки PNG/PDF.
  - `email_signature.py` — HTML email-подписи.
  - `presentation.py` — PPTX/PDF.
  - `proposal.py` — DOCX/PDF.
- `src/web/` — статический HTML/CSS/JS фронтенд.
- `data/` — бренд-бук и рабочие данные (не в Git).
- `output/` — сгенерированные файлы (не в Git).
- `uploads/` — загруженные логотипы (не в Git).

Подробнее см. [references/structure.md](references/structure.md).

## Правила изменений

1. **Новый тип материала** — добавь генератор в `src/generators/`, эндпоинт в `src/api/routes.py` и UI-элемент в `src/web/index.html`.
2. **Логотипы** — поддерживаются PNG, JPG, SVG. Для встраивания используй `core.images.prepare_logo()` или `core.images.open_logo()`; SVG автоматически конвертируется в PNG.
3. **Пути и конфигурация** — все папки брать из `src/core/config.py`. Не хардкодить пути.
4. **Зависимости** — при добавлении библиотеки обнови `requirements.txt`.
5. **Веб-интерфейс** — статика без фреймворков. Стилистика: Open Sans/Inter, акценты `#5A4BFF` и `#FF5B24`, фон `#FAFAF8`, текст `#1F1F1E`.
6. **README** — при новой фиче обнови разделы «Основная функция», «Поддерживаемые материалы», «MVP», «Структура проекта» и примеры команд.
7. **Тесты** — при изменении генераторов запусти `python -m pytest tests/ -v` и убедись, что они проходят.

## Проверка ошибок

Перед тем как показать результат Katy:

1. **Окружение**: активирован `.venv`, установлены зависимости.
2. **Импорты**:
   ```bash
   python -c "import sys; sys.path.insert(0,'src'); from generators import business_card, email_signature, presentation, proposal; print('OK')"
   ```
3. **Веб-сервер**: запусти `python web.py`, открой `http://127.0.0.1:8000`, сгенерируй визитку.
4. **CLI**:
   ```bash
   python run.py business-card --input demo/sample-inputs/employee.json
   python run.py email-signature --input demo/sample-inputs/employee.json
   python run.py presentation --input demo/sample-inputs/client.json
   python run.py proposal --input demo/sample-inputs/proposal.json
   ```
5. **PDF**: для PPTX/DOCX в PDF нужен LibreOffice; PNG → PDF работает без него.
6. **Консоль**: проверь на `ModuleNotFoundError` и `FileNotFoundError`.
   - Если `brandbook.json` отсутствует — загрузи бренд-бук через веб или CLI: `python run.py upload-brandbook --file data/brandbook.json`.
   - Если падает конвертация PPTX/DOCX в PDF — проверь, что LibreOffice установлен и доступен в PATH.

## Обновление README

- Отражай новые функции и форматы.
- Проверяй, что все примеры команд из README реально работают.
- Если изменился UI — обнови `docs/screenshot-web-ui.png` (сделай скриншот через Playwright в полный рост страницы).

## Подготовка к публикации

1. Убедись, что в индекс не попали `.venv/`, `data/`, `output/`, `uploads/`, `.env`, `__pycache__/` — `.gitignore` уже исключает их.
2. Обнови `README.md` и документацию в `docs/`, если проект изменился.
3. Запусти тесты: `python -m pytest tests/ -v`.
4. Актуализируй скриншот веб-интерфейса.
5. Только после подтверждения Katy выполняй:
   ```bash
   git add .
   git commit -m "..."
   git push origin master
   ```
   Сообщение коммита должно заканчиваться строкой:
   ```
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

## Ограничения

- Не выходить за пределы рабочей папки проекта без разрешения.
- Не отправлять письма и сообщения от имени Katy.
- Не редактировать готовые/согласованные договоры и документы без запроса.
- Не удалять и не переименовывать существующие файлы без подтверждения.
