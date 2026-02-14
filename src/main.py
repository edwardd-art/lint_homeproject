#!/usr/bin/env python3
"""Основной скрипт для работы с реальными данными"""

import os

from mask import get_mask_account, get_mask_card_number  # ДОБАВИЛИ ИМПОРТ
from src import convert_amount_to_rub, read_json_file


def main():
    # Читаем транзакции
    file_path = os.path.join("../data", "operations.json")
    transactions = read_json_file(file_path)

    print(f"Загружено транзакций: {len(transactions)}")
    print("=" * 60)

    # ДОБАВЛЯЕМ ТЕСТИРОВАНИЕ МАСКИРОВАНИЯ
    print("\n🔐 Тестирование маскирования:")
    test_card = "1234567890123456"
    masked_card = get_mask_card_number(test_card)
    print(f"  Карта: {masked_card}")

    test_account = "40817810099910004312"
    masked_account = get_mask_account(test_account)
    print(f"  Счет: {masked_account}")
    print("=" * 60)

    # Обрабатываем первые 5 транзакций для примера
    for i, transaction in enumerate(transactions[:5], 1):
        print(f"\n📝 Транзакция #{i}:")
        print(f"  ID: {transaction.get('id', 'N/A')}")
        print(f"  Описание: {transaction.get('description', 'N/A')}")

        # ДОБАВЛЯЕМ МАСКИРОВАНИЕ НОМЕРОВ КАРТ И СЧЕТОВ ИЗ ТРАНЗАКЦИЙ
        from_field = transaction.get('from', '')
        to_field = transaction.get('to', '')

        if from_field:
            # Пробуем извлечь номер карты/счета и замаскировать
            words = from_field.split()
            if words and words[-1].isdigit():
                number = words[-1]
                if len(number) == 16:  # Это карта
                    masked_number = get_mask_card_number(number)
                    from_field = ' '.join(words[:-1] + [masked_number])
                    print(f"  Откуда: {from_field}")
                elif len(number) > 16:  # Это счет
                    masked_number = get_mask_account(number)
                    from_field = ' '.join(words[:-1] + [masked_number])
                    print(f"  Откуда: {from_field}")
            else:
                print(f"  Откуда: {from_field}")
        else:
            print("  Откуда: Не указано")

        if to_field:
            words = to_field.split()
            if words and words[-1].isdigit():
                number = words[-1]
                if len(number) == 16:  # Это карта
                    masked_number = get_mask_card_number(number)
                    to_field = ' '.join(words[:-1] + [masked_number])
                    print(f"  Куда: {to_field}")
                elif len(number) > 16:  # Это счет
                    masked_number = get_mask_account(number)
                    to_field = ' '.join(words[:-1] + [masked_number])
                    print(f"  Куда: {to_field}")
            else:
                print(f"  Куда: {to_field}")
        else:
            print("  Куда: Не указано")

        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "N/A")
        currency_info = operation_amount.get("currency", {})
        currency_name = currency_info.get("name", "N/A")
        currency_code = currency_info.get("code", "N/A")

        print(f"  Сумма: {amount} {currency_name} ({currency_code})")

        # Конвертируем
        amount_rub = convert_amount_to_rub(transaction)

        if amount_rub is not None:
            print(f"  💰 В рублях: {amount_rub:.2f} RUB")
        else:
            print("  ❌ Ошибка конвертации")

    print("\n" + "=" * 60)
    print("✅ Обработка завершена")
    print("📁 Проверь папку 'logs' - там должны быть оба файла: mask.log и utils.log")


if __name__ == "__main__":
    main()
