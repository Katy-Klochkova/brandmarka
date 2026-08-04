# Техническое задание MVP

## Стек

- **Язык:** Python 3.12
- **Backend:** FastAPI
- **Frontend:** статический HTML + JS (без фреймворков)
- **Генерация документов:** ReportLab / python-pptx / python-docx
- **QR-коды:** qrcode
- **LLM:** Anthropic Claude API
- **Хранение:** JSON-файлы на диске (для MVP)

## Модули

| Модуль | Ответственность |
|--------|-----------------|
| `core.brand` | Загрузка, валидация и чтение бренд-бука |
| `core.renderer` | Рендеринг PDF, PNG, PPTX, DOCX |
| `core.exporter` | Упаковка файлов и отдача пользователю |
| `core.storage` | Сохранение проектов и настроек |
| `generators.*` | Генерация контента через LLM + шаблоны |
| `api.routes` | HTTP-эндпоинты |
| `web.*` | Простой интерфейс |
| `cli.brandmarka` | Консольная генерация |

## API (кратко)

- `POST /api/brandbook` — загрузить бренд-бук.
- `GET /api/brandbook` — получить текущий бренд-бук.
- `POST /api/business-card` — сгенерировать визитку.
- `POST /api/email-signature` — сгенерировать email-подпись.
- `POST /api/presentation` — сгенерировать презентацию.
- `POST /api/proposal` — сгенерировать КП.

## Данные

### BrandBook

```json
{
  "company": "ООО Пример",
  "logo_url": "logo.png",
  "colors": { "primary": "#1E40AF", "secondary": "#F59E0B", "text": "#111827" },
  "fonts": { "heading": "Inter", "body": "Inter" },
  "contacts": { "phone": "+7 495 000-00-00", "email": "info@example.com", "site": "example.com" },
  "tone": "деловой, современный, без канцелярита"
}
```

### BusinessCardInput

```json
{
  "full_name": "Иванов Иван Иванович",
  "position": "Руководитель отдела продаж",
  "phone": "+7 900 123-45-67",
  "email": "ivanov@example.com",
  "telegram": "@ivanov_example"
}
```

### PresentationInput

```json
{
  "client_name": "ООО Клиент",
  "project_goal": "внедрение системы вибродиагностики",
  "key_points": ["опыт 15 лет", "200+ внедрений", "сервис 24/7"],
  "pages": 8
}
```

### ProposalInput

```json
{
  "client_name": "ООО Клиент",
  "services": [{"name": "Поставка оборудования", "price": 1200000}],
  "terms": "30 рабочих дней",
  "payment": "50/50"
}
```
