#!/usr/bin/env python3
"""Тестирование с реальными данными из operations.json"""

import os
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import read_json_file
from external_api import convert_amount_to_rub


def test_with_real_data():
    """Тест с реальными данными из файла"""
    print("🧪 Тестирование с реальными данными из operations.json")
    print("=" * 60)

    # 1. Чтение файла
    file_path = "data/operations.json"
    transactions = read_json_file(file_path)

    print(f"Загружено транзакций: {len(transactions)}")

    # 2. Тестируем несколько транзакций
    test_count = min(10, len(transactions))  # Первые 10

    print(f"\nТестируем первые {test_count} транзакций:")
    print("-" * 60)

    for i in range(test_count):
        transaction = transactions[i]
        print(f"\nТранзакция #{i + 1}:")
        print(f"  ID: {transaction.get('id', 'N/A')}")
        print(f"  Описание: {transaction.get('description', 'N/A')}")

        # Получаем информацию о сумме
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "N/A")
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code", "N/A")
        currency_name = currency_info.get("name", "N/A")

        print(f"  Сумма: {amount} {currency_name} ({currency_code})")

        # Конвертация
        result = convert_amount_to_rub(transaction)

        if result is not None:
            print(f"  В рублях: {result:.2f} RUB")
            print(f"  Тип результата: {type(result).__name__}")

            # Для RUB результат должен быть равен сумме
            if currency_code == "RUB":
                expected = float(amount)
                if abs(result - expected) < 0.01:
                    print("  ✅ RUB конвертирован правильно")
                else:
                    print(f"  ❌ Ошибка: ожидалось {expected}, получено {result}")
            else:
                print(f"  ✅ {currency_code} сконвертирован в RUB")
        else:
            print("  ❌ Ошибка конвертации")

    # 3. Статистика по всем транзакциям
    print("\n" + "=" * 60)
    print("Статистика по всем транзакциям:")
    print("-" * 60)

    rub_count = 0
    usd_count = 0
    other_count = 0
    successful_conversions = 0
    failed_conversions = 0

    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code", "")

        if currency_code == "RUB":
            rub_count += 1
        elif currency_code == "USD":
            usd_count += 1
        else:
            other_count += 1

        # Пробуем конвертировать
        result = convert_amount_to_rub(transaction)
        if result is not None:
            successful_conversions += 1
        else:
            failed_conversions += 1

    print(f"  Всего транзакций: {len(transactions)}")
    print(f"  RUB: {rub_count}")
    print(f"  USD: {usd_count}")
    print(f"  Другие валюты: {other_count}")
    print(f"  Успешных конвертаций: {successful_conversions}")
    print(f"  Ошибок конвертации: {failed_conversions}")

    return successful_conversions > 0


def main():
    """Основная функция"""
    # Устанавливаем API ключ
    os.environ["API_KEY"] = "PT2oRUi3Bv1H9LJ5IHGGcysDgPIgnHC9"

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ С РЕАЛЬНЫМИ ДАННЫМИ")
    print("=" * 60)

    if test_with_real_data():
        print("\n✅ Тестирование успешно!")
        print("Функции работают с реальными данными из operations.json")
    else:
        print("\n❌ Есть проблемы с обработкой данных")

    print("=" * 60)


if __name__ == "__main__":
    main()