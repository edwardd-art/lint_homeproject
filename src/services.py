# src/services.py
import json
import re
from typing import Any, Dict, List


def search_transactions_service(transactions: List[Dict[str, Any]], search_query: str) -> str:
    """
    Сервис поиска транзакций по описанию или категории.

    Args:
        transactions: Список словарей с транзакциями (уже нормализованными)
        search_query: Строка для поиска (регистронезависимый поиск)

    Returns:
        JSON-строка с найденными транзакциями
    """
    if not transactions or not search_query:
        return json.dumps([], ensure_ascii=False)

    search_lower = search_query.lower()
    result = []

    for t in transactions:
        description = str(t.get('description', '')).lower()
        category = str(t.get('category', '')).lower()

        if search_lower in description or search_lower in category:
            result.append(t)

    return json.dumps(result, ensure_ascii=False, indent=2)


def search_phone_numbers(transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск транзакций, содержащих в описании мобильные номера телефонов.

    Поддерживаемые форматы:
    - +7 921 11-22-33
    - +7 995 555-55-55
    - +7 981 333-44-55
    - 8 921 111-22-33
    """
    # Регулярное выражение для поиска телефонных номеров
    phone_pattern = re.compile(
        r'(\+7|8)?[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}'
    )

    result = []
    for t in transactions:
        description = str(t.get('description', ''))
        if phone_pattern.search(description):
            result.append(t)

    return json.dumps(result, ensure_ascii=False, indent=2)


def search_transfers_to_individuals(transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск переводов физическим лицам.

    Условия:
    - Категория = 'Переводы'
    - В описании есть имя и первая буква фамилии с точкой (например, "Константин Л.")
    """
    result = []
    for t in transactions:
        category = str(t.get('category', ''))
        description = str(t.get('description', ''))

        # Проверяем категорию
        if category.lower() != 'переводы':
            continue

        # Проверяем формат "Имя Фамилия_буква."
        # Примеры: "Константин Л.", "Сергей З.", "Артем П."
        name_pattern = re.compile(r'[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.')

        if name_pattern.search(description):
            result.append(t)

    return json.dumps(result, ensure_ascii=False, indent=2)