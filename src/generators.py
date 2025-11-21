"""
Модуль для работы с генераторами обработки финансовых данных.
"""

from typing import Iterator, Dict, Any
import json


def filter_by_currency(transactions: list, currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, 'USD')

    Yields:
        Словари транзакций в указанной валюте
    """
    for transaction in transactions:
        if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency:
            yield transaction


def transaction_descriptions(transactions: list) -> Iterator[str]:
    """
    Генерирует описания транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описания транзакций
    """
    for transaction in transactions:
        yield transaction.get('description', '')


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start: Начальный номер карты (целое число)
        end: Конечный номер карты (целое число)

    Yields:
        Номера карт в формате 'XXXX XXXX XXXX XXXX'
    """
    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        formatted_card = ' '.join([card_str[i:i + 4] for i in range(0, 16, 4)])
        yield formatted_card
