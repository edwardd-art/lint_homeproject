# src/views.py (начало файла)
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

# Добавляем текущую папку в путь
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()

logger = logging.getLogger('views')


# API ключ для курсов валют
EXCHANGE_API_KEY = os.getenv('API_KEY')
EXCHANGE_API_URL = os.getenv('EXCHANGE_API_URL', 'https://api.apilayer.com/exchangerates_data')


def load_user_settings() -> Dict[str, Any]:
    """
    Загружает настройки пользователя из файла user_settings.json.
    """
    settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_settings.json')
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Файл настроек не найден: {settings_path}")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL"]}
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга user_settings.json: {e}")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL"]}


def get_greeting() -> str:
    """
    Возвращает приветствие в зависимости от текущего времени.
    """
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# src/views.py - исправленные функции

# src/views.py - исправленные функции

def get_card_data(transactions_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает данные по каждой карте."""
    card_data = []

    # Используем правильные названия колонок
    if 'сумма_операции' not in transactions_df.columns:
        return []

    # Фильтруем расходы (отрицательные суммы)
    expenses_df = transactions_df[transactions_df['сумма_операции'] < 0].copy()
    expenses_df['сумма_операции'] = expenses_df['сумма_операции'].abs()

    if 'номер_карты' not in transactions_df.columns:
        return []

    for card, group in expenses_df.groupby('номер_карты'):
        if pd.isna(card) or card == '':
            continue
        card_last4 = str(card)[-4:] if len(str(card)) >= 4 else str(card)
        total_expenses = group['сумма_операции'].sum()
        cashback = int(total_expenses // 100)

        card_data.append({
            "last_digits": card_last4,
            "total_expenses": round(total_expenses, 2),
            "cashback": cashback
        })

    return card_data


def get_top_transactions(transactions_df: pd.DataFrame, limit: int = 5) -> List[Dict[str, Any]]:
    """Возвращает топ-N транзакций по сумме платежа."""
    if 'сумма_платежа' not in transactions_df.columns:
        return []

    sorted_df = transactions_df.sort_values('сумма_платежа', ascending=False)
    top_n = sorted_df.head(limit)

    result = []
    for _, row in top_n.iterrows():
        result.append({
            "date": row.get('дата_платежа', ''),
            "amount": abs(row.get('сумма_платежа', 0)),
            "category": row.get('категория', ''),
            "description": row.get('описание', '')
        })

    return result


def get_exchange_rates(currencies: List[str]) -> Dict[str, float]:
    """Временная заглушка для курсов валют."""
    return {curr: 95.50 for curr in currencies}  # 1 RUB = 95.50 USD/EUR


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Временная заглушка для цен акций."""
    mock_prices = {
        "AAPL": 175.50,
        "AMZN": 145.30,
        "GOOGL": 140.20,
        "MSFT": 420.75,
        "TSLA": 250.15
    }
    return [{"stock": stock, "price": mock_prices.get(stock, 100.0)} for stock in stocks]


def main_views(date_str: str, transactions_df: Optional[pd.DataFrame] = None) -> str:
    """
    Главная функция модуля views.

    Args:
        date_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
        transactions_df: DataFrame с транзакциями (если не передан, загружается из файла)

    Returns:
        JSON-строка с данными для главной страницы
    """
    logger.info(f"Вызов main_views с датой: {date_str}")

    # Определяем диапазон данных: с начала месяца по указанную дату
    try:
        input_date = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
        start_of_month = input_date.replace(day=1)
    except Exception as e:
        logger.error(f"Ошибка парсинга даты: {e}")
        start_of_month = datetime.now().replace(day=1)
        input_date = datetime.now()

    # Загружаем транзакции, если не переданы
    if 'дата операции' in transactions_df.columns:
        transactions_df['дата операции'] = pd.to_datetime(transactions_df['дата операции'], dayfirst=True)
        mask = (transactions_df['дата операции'] >= pd.Timestamp(start_of_month)) & \
               (transactions_df['дата операции'] <= pd.Timestamp(input_date))
        filtered_df = transactions_df[mask]
    else:
        filtered_df = transactions_df

    # Загружаем настройки пользователя
    settings = load_user_settings()
    currencies = settings.get('user_currencies', ['USD', 'EUR'])
    stocks = settings.get('user_stocks', ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA'])

    # Формируем JSON-ответ
    result = {
        "greeting": get_greeting(),
        "cards": get_card_data(filtered_df),
        "top_transactions": get_top_transactions(filtered_df, 5),
        "currency_rates": get_exchange_rates(currencies),
        "stock_prices": get_stock_prices(stocks)
    }

    logger.info("JSON-ответ для главной страницы успешно сформирован")
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Тестовый запуск
    test_result = main_views("2021-12-31 16:44:00")
    print(test_result)