# src/reports.py
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd

# Добавляем текущую папку в путь для импорта декоратора
sys.path.insert(0, os.path.dirname(__file__))

from decorators import log


@log(filename='reports.log')
def spending_by_category(
        transactions_df: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> str:
    """
    Возвращает траты по заданной категории за последние 3 месяца.

    Args:
        transactions_df: DataFrame с транзакциями
        category: Название категории
        date: Опциональная дата в формате 'YYYY-MM-DD'

    Returns:
        JSON-строка с тратами по категории
    """
    df = transactions_df.copy()

    # Определяем целевую дату
    if date is None:
        # Берем максимальную дату из данных
        df['дата_операции'] = pd.to_datetime(df['дата_операции'], dayfirst=True)
        target_date = df['дата_операции'].max()
    else:
        target_date = datetime.strptime(date, '%Y-%m-%d')

    three_months_ago = target_date - timedelta(days=90)

    # Проверка наличия колонок
    required_cols = ['дата_операции', 'категория', 'сумма_операции']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return json.dumps({"error": f"Отсутствуют колонки: {missing_cols}"}, ensure_ascii=False)

    df['дата_операции'] = pd.to_datetime(df['дата_операции'], dayfirst=True)

    mask = (df['категория'].str.lower() == category.lower()) & \
           (df['дата_операции'] >= pd.Timestamp(three_months_ago)) & \
           (df['дата_операции'] <= pd.Timestamp(target_date)) & \
           (df['сумма_операции'] < 0)

    filtered_df = df[mask]
    total_spent = abs(filtered_df['сумма_операции'].sum())

    result = {
        "category": category,
        "period": f"{three_months_ago.strftime('%Y-%m-%d')} - {target_date.strftime('%Y-%m-%d')}",
        "total_spent": round(total_spent, 2),
        "transactions_count": len(filtered_df)
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


@log(filename='reports.log')
@log(filename='reports.log')
def spending_by_day_of_week(
        transactions_df: pd.DataFrame,
        date: Optional[str] = None
) -> str:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.
    """
    df = transactions_df.copy()

    # Определяем целевую дату
    if date is None:
        df['дата_операции'] = pd.to_datetime(df['дата_операции'], dayfirst=True)
        target_date = df['дата_операции'].max()
    else:
        target_date = datetime.strptime(date, '%Y-%m-%d')

    three_months_ago = target_date - timedelta(days=90)

    # Проверка наличия колонок
    if 'дата_операции' not in df.columns or 'сумма_операции' not in df.columns:
        return json.dumps({"error": "Отсутствуют необходимые колонки"}, ensure_ascii=False)

    df['дата_операции'] = pd.to_datetime(df['дата_операции'], dayfirst=True)

    # Фильтруем по дате и только расходы
    mask = (df['дата_операции'] >= pd.Timestamp(three_months_ago)) & \
           (df['дата_операции'] <= pd.Timestamp(target_date)) & \
           (df['сумма_операции'] < 0)

    filtered_df = df[mask].copy()
    filtered_df['сумма_операции'] = filtered_df['сумма_операции'].abs()

    # Ручное определение дня недели (без locale, для Windows)
    days_map = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    filtered_df['day_of_week'] = filtered_df['дата_операции'].dt.weekday.map(days_map)

    # Группируем по дням недели
    weekday_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    avg_spending = filtered_df.groupby('day_of_week')['сумма_операции'].mean().round(2)

    # Приводим к нужному порядку
    result = {}
    for day in weekday_order:
        result[day] = float(avg_spending.get(day, 0))

    return json.dumps(result, ensure_ascii=False, indent=2)


@log(filename='reports.log')
def spending_by_workday(
        transactions_df: pd.DataFrame,
        date: Optional[str] = None
) -> str:
    """
    Возвращает средние траты в рабочие и выходные дни за последние 3 месяца.

    Args:
        transactions_df: DataFrame с транзакциями
        date: Опциональная дата в формате 'YYYY-MM-DD'

    Returns:
        JSON-строка со средними тратами в рабочие и выходные дни
    """
    df = transactions_df.copy()

    # Определяем целевую дату
    if date is None:
        # Берем максимальную дату из данных
        df['дата_операции'] = pd.to_datetime(df['дата_операции'], dayfirst=True)
        target_date = df['дата_операции'].max()
    else:
        target_date = datetime.strptime(date, '%Y-%m-%d')

    three_months_ago = target_date - timedelta(days=90)

    # Проверка наличия колонок
    if 'дата_операции' not in df.columns or 'сумма_операции' not in df.columns:
        return json.dumps({"error": "Отсутствуют необходимые колонки"}, ensure_ascii=False)

    df['дата_операции'] = pd.to_datetime(df['дата_операции'], dayfirst=True)

    # Фильтруем по дате и только расходы
    mask = (df['дата_операции'] >= pd.Timestamp(three_months_ago)) & \
           (df['дата_операции'] <= pd.Timestamp(target_date)) & \
           (df['сумма_операции'] < 0)

    filtered_df = df[mask].copy()
    filtered_df['сумма_операции'] = filtered_df['сумма_операции'].abs()

    # Определяем рабочие (0-4) и выходные (5-6) дни
    filtered_df['is_weekend'] = filtered_df['дата_операции'].dt.weekday >= 5

    workday_avg = filtered_df[~filtered_df['is_weekend']]['сумма_операции'].mean()
    weekend_avg = filtered_df[filtered_df['is_weekend']]['сумма_операции'].mean()

    result = {
        "workday_avg": round(workday_avg if not pd.isna(workday_avg) else 0, 2),
        "weekend_avg": round(weekend_avg if not pd.isna(weekend_avg) else 0, 2),
        "period": f"{three_months_ago.strftime('%Y-%m-%d')} - {target_date.strftime('%Y-%m-%d')}"
    }

    return json.dumps(result, ensure_ascii=False, indent=2)