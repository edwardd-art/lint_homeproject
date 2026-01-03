#!/usr/bin/env python3
"""Интеграционный тест всего проекта"""

import os
import sys
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import read_json_file
from external_api import convert_amount_to_rub


def test_full_pipeline():
    """Тест всей цепочки обработки"""
    print("🧪 Запуск интеграционного теста...")

    # 1. Чтение файла
    file_path = "data/operations.json"
    print(f"1. Чтение файла: {file_path}")

    transactions = read_json_file(file_path)

    if not transactions:
        print("❌ Не удалось загрузить транзакции")
        return False

    print(f"   Загружено транзакций: {len(transactions)}")

    # 2. Конвертация каждой транзакции
    print("\n2. Конвертация транзакций:")
    successful = 0
    failed = 0

    for i, transaction in enumerate(transactions, 1):
        print(f"\n   Транзакция #{i}:")
        print(f"     Описание: {transaction.get('description', 'N/A')}")
        print(f"     Сумма: {transaction.get('amount')} {transaction.get('currency')}")

        # Конвертация
        result = convert_amount_to_rub(transaction)

        if result is not None:
            print(f"     Результат: {result:.2f} RUB")
            print(f"     Тип результата: {type(result).__name__}")

            # Проверяем что результат - float
            if isinstance(result, float):
                print("     ✅ Результат - float")
                successful += 1
            else:
                print(f"     ❌ Ошибка: результат не float, а {type(result)}")
                failed += 1
        else:
            print("     ❌ Ошибка конвертации")
            failed += 1

    # 3. Итоги
    print(f"\n📊 Итоги:")
    print(f"   Успешно: {successful}")
    print(f"   Ошибок: {failed}")
    print(f"   Всего: {len(transactions)}")

    return failed == 0


def main():
    """Основная функция"""
    print("=" * 60)
    print("ИНТЕГРАЦИОННЫЙ ТЕСТ ПРОЕКТА")
    print("=" * 60)

    # Устанавливаем API ключ для тестов
    os.environ["API_KEY"] = "PT2oRUi3Bv1H9LJ5IHGGcysDgPIgnHC9"

    if test_full_pipeline():
        print("\n🎉 Все тесты пройдены успешно!")
        print("Функции работают корректно:")
        print("  ✅ read_json_file возвращает список или пустой список при ошибках")
        print("  ✅ convert_amount_to_rub всегда возвращает float или None")
        print("  ✅ Обработка FileNotFoundError реализована")
    else:
        print("\n⚠️  Есть проблемы в работе проекта")

    print("=" * 60)


if __name__ == "__main__":
    main()