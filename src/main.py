# src/main.py (начало файла)
import sys
import os

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from datetime import datetime

import pandas as pd

from .reports import spending_by_category, spending_by_day_of_week, spending_by_workday
from .services import (
    search_phone_numbers,
    search_transactions_service,
    search_transfers_to_individuals,
)
from .views import main_views


def load_transactions() -> pd.DataFrame:
    """Загружает транзакции из Excel файла."""
    # Пробуем .xlsx
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')

    # Если не найден, пробуем .xls
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xls')

    print(f"📂 Загрузка файла: {file_path}")
    print(f"📁 Файл существует: {os.path.exists(file_path)}")

    df = pd.read_excel(file_path)

    df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]

    # ДИАГНОСТИКА
    print("=" * 60)
    print("🔍 НАЙДЕНЫ КОЛОНКИ В EXCEL:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. '{col}'")
    print("=" * 60)

    return df


def main():
    """Главная функция для демонстрации работы всех модулей."""
    print("=" * 60)
    print("КУРСОВАЯ РАБОТА: Анализ банковских транзакций")
    print("=" * 60)

    # Загружаем данные
    df = load_transactions()
    print(f"✅ Загружено транзакций: {len(df)}")

    # Показываем первые 2 строки для примера
    print("\n📊 ПЕРВЫЕ 2 ТРАНЗАКЦИИ:")
    print(df.head(2).to_string())
    print("=" * 60)

    # 1. Главная страница
    print("\n" + "=" * 60)
    print("1. ГЛАВНАЯ СТРАНИЦА")
    print("=" * 60)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    views_result = main_views(current_time, df)
    print(json.dumps(json.loads(views_result), indent=2, ensure_ascii=False)[:1000] + "...")

    # 2. Поиск по телефонным номерам
    print("\n" + "=" * 60)
    print("2. ПОИСК ПО ТЕЛЕФОННЫМ НОМЕРАМ")
    print("=" * 60)
    phone_result = search_phone_numbers(df.to_dict('records'))
    print(phone_result[:500] + "..." if len(phone_result) > 500 else phone_result)

    # 3. Поиск переводов физлицам
    print("\n" + "=" * 60)
    print("3. ПОИСК ПЕРЕВОДОВ ФИЗИЧЕСКИМ ЛИЦАМ")
    print("=" * 60)
    transfers_result = search_transfers_to_individuals(df.to_dict('records'))
    print(transfers_result[:500] + "..." if len(transfers_result) > 500 else transfers_result)

    # 4. Отчет: траты по категории
    print("\n" + "=" * 60)
    print("4. ОТЧЕТ: ТРАТЫ ПО КАТЕГОРИИ 'Супермаркеты'")
    print("=" * 60)
    category_result = spending_by_category(df, "Супермаркеты")
    print(category_result)

    # 5. Отчет: траты по дням недели
    print("\n" + "=" * 60)
    print("5. ОТЧЕТ: ТРАТЫ ПО ДНЯМ НЕДЕЛИ")
    print("=" * 60)
    weekday_result = spending_by_day_of_week(df)
    print(weekday_result)

    # 6. Отчет: траты в рабочие/выходные дни
    print("\n" + "=" * 60)
    print("6. ОТЧЕТ: ТРАТЫ В РАБОЧИЕ И ВЫХОДНЫЕ ДНИ")
    print("=" * 60)
    workday_result = spending_by_workday(df)
    print(workday_result)

    print("\n" + "=" * 60)
    print("✅ Все модули успешно выполнены!")
    print("📁 Логи записаны в файл reports.log")
    print("=" * 60)


if __name__ == "__main__":
    main()