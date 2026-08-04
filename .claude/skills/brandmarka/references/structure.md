# Структура Brandmarka

```
brandmarka/
├── .claude/
│   └── skills/
│       └── brandmarka/
│           ├── SKILL.md              # этот скилл
│           └── references/
│               └── structure.md      # это файл
├── data/                             # бренд-бук и рабочие данные (не в Git)
│   └── brandbook.json
├── demo/                             # примеры входных JSON
├── design/                           # шаблоны бренд-бука и промпты
├── docs/                             # документация и скриншоты
│   └── screenshot-web-ui.png
├── output/                           # сгенерированные файлы (не в Git)
├── uploads/                          # загруженные логотипы (не в Git)
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                 # FastAPI эндпоинты и статика
│   ├── cli/
│   │   ├── __init__.py
│   │   └── brandmarka.py             # консольная утилита
│   ├── core/
│   │   ├── __init__.py
│   │   ├── brand.py                  # работа с brandbook.json
│   │   ├── config.py                 # пути и переменные окружения
│   │   ├── exporter.py               # PNG → PDF, DOCX/PPTX → PDF
│   │   ├── images.py                 # обработка логотипов PNG/JPG/SVG
│   │   └── llm.py                    # Claude API (подготовлено)
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── business_card.py          # PNG/PDF визитки
│   │   ├── email_signature.py        # HTML email-подписи
│   │   ├── presentation.py           # PPTX/PDF презентации
│   │   └── proposal.py               # DOCX/PDF коммерческие предложения
│   └── web/
│       └── index.html                # статический веб-интерфейс
├── .env.example                      # шаблон API-ключа
├── .gitignore                        # исключения (.venv, data, output, uploads, .env)
├── README.md                         # основная документация
├── requirements.txt                  # зависимости Python
├── run.py                            # запуск CLI
└── web.py                            # запуск веб-сервера
```

## Ответственность файлов

| Файл | За что отвечает |
|------|-----------------|
| `web.py` | Запуск Uvicorn с `reload=True`, приложение `src/api/routes:app`. |
| `run.py` | Точка входа CLI: добавляет `src/` в `sys.path` и вызывает `cli.brandmarka.main()`. |
| `src/api/routes.py` | Эндпоинты `/api/brandbook`, `/api/business-card`, `/api/email-signature`, `/api/presentation`, `/api/proposal`; раздача `src/web/` через `/static` и `uploads/` через `/uploads`. |
| `src/core/brand.py` | `load()` / `save()` для `data/brandbook.json`, простая валидация. |
| `src/core/config.py` | Пути `BASE_DIR`, `DATA_DIR`, `OUTPUT_DIR`, `UPLOADS_DIR`; `ANTHROPIC_API_KEY`. |
| `src/core/images.py` | `_svg_to_png()`, `prepare_logo()`, `open_logo()` — подготовка логотипа для генераторов. |
| `src/core/exporter.py` | `png_to_pdf()` и `office_to_pdf()` (LibreOffice). |
| `src/generators/*.py` | Рендер конкретных материалов на основе бренд-бука и входных данных. |
| `src/web/index.html` | Весь фронтенд: загрузка бренд-бука/логотипа, выбор материала, формы, запросы к API. |
