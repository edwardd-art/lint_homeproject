#!/usr/bin/env python3
"""Основной скрипт для работы с реальными данными"""

import os
from src import read_json_file, convert_amount_to_rub


def main():
    # Читаем транзакции
    file_path = os.path.join("data", "operations.json")
    transactions = read_json_file(file_path)

    print(f"Загружено транзакций: {len(transactions)}")
    print("=" * 60)

    # Обрабатываем первые 5 транзакций для примера
    for i, transaction in enumerate(transactions[:5], 1):
        print(f"\nТранзакция #{i}:")
        print(f"  ID: {transaction.get('id', 'N/A')}")
        print(f"  Описание: {transaction.get('description', 'N/A')}")

        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "N/A")
        currency_info = operation_amount.get("currency", {})
        currency_name = currency_info.get("name", "N/A")
        currency_code = currency_info.get("code", "N/A")

        print(f"  Сумма: {amount} {currency_name} ({currency_code})")

        # Конвертируем
        amount_rub = convert_amount_to_rub(transaction)

        if amount_rub is not None:
            print(f"  В рублях: {amount_rub:.2f} RUB")
        else:
            print("  ❌ Ошибка конвертации")

    print("\n" + "=" * 60)
    print("✅ Обработка завершена")


if __name__ == "__main__":
    main()
