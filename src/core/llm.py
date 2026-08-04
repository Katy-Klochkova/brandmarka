"""Работа с Anthropic Claude API."""

import json

from anthropic import Anthropic

from core.config import ANTHROPIC_API_KEY


def _get_client() -> Anthropic:
    """Создать клиента Claude."""
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY не найден. "
            "Создай файл .env в корне проекта и добавь строку:\n"
            "ANTHROPIC_API_KEY=sk-ant-..."
        )
    return Anthropic(api_key=ANTHROPIC_API_KEY)


def ask(
    prompt: str,
    system: str = "Ты полезный ассистент.",
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2000,
) -> str:
    """Отправить промпт в Claude и вернуть текст ответа."""
    client = _get_client()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def ask_json(
    prompt: str,
    system: str = "Ты полезный ассистент. Всегда отвечай строго в формате JSON.",
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2000,
) -> dict:
    """Отправить промпт в Claude и вернуть распарсенный JSON."""
    text = ask(prompt=prompt, system=system, model=model, max_tokens=max_tokens)
    # Claude иногда оборачивает JSON в ```json ... ```
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1].strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    return json.loads(cleaned)
