# Промпты для генерации

## Визитка

```
На основе бренд-бука компании {company} составь текст для визитки сотрудника:
- ФИО: {full_name}
- Должность: {position}
- Телефон: {phone}
- Email: {email}
- Telegram: {telegram}

Тон: {tone}. Используй фирменные цвета и шрифты. Верни JSON с полями:
front_lines, back_lines, primary_color, secondary_color.
```

## Презентация

```
Составь клиентскую презентацию для компании {client_name}.
Цель проекта: {project_goal}.
Ключевые тезисы: {key_points}.
Количество слайдов: {pages}.

Тон: {tone}. Начинай с титульного слайда, заканчивай призывом к действию.
Верни JSON: массив slides, каждый с полями title и bullets.
```

## Коммерческое предложение

```
Составь коммерческое предложение от {company} для {client_name}.
Услуги: {services}.
Сроки: {terms}.
Условия оплаты: {payment}.

Тон: {tone}. Верни JSON с полями intro, services, terms, payment, contacts.
```
