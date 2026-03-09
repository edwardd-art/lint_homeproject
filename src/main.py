"""Основной скрипт для работы с реальными данными"""

import argparse
import os
from typing import Any, Dict  # Добавь импорт

from src.mask import get_mask_account, get_mask_card_number
from src.utils import read_transactions


def print_transaction_details(transaction: Dict[str, Any], index: int) -> None:
    """Выводит детали транзакции"""
    print(f"\n📝 Транзакция #{index}:")
    print(f"  ID: {transaction.get('id', transaction.get('ID', 'N/A'))}")
    print(f"  Описание: {transaction.get('description', transaction.get('Описание', 'N/A'))}")

    # Маскирование номеров карт и счетов из транзакций
    from_field = transaction.get('from', transaction.get('Откуда', ''))
    to_field = transaction.get('to', transaction.get('Куда', ''))

    if from_field:
        words = str(from_field).split()
        if words and words[-1].replace(' ', '').isdigit():
            number = words[-1].replace(' ', '')
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
        words = str(to_field).split()
        if words and words[-1].replace(' ', '').isdigit():
            number = words[-1].replace(' ', '')
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

    # Для разных форматов могут быть разные названия полей
    amount = transaction.get('amount', transaction.get('Сумма', 'N/A'))
    currency = transaction.get('currency', transaction.get('Валюта', 'RUB'))

    print(f"  Сумма: {amount} {currency}")


def main() -> None:
    """Главная функция программы"""
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Чтение финансовых транзакций из разных форматов')
    parser.add_argument('--file', type=str, default='operations.json',
                        help='Имя файла с транзакциями (из папки data/)')
    parser.add_argument('--limit', type=int, default=5,
                        help='Количество транзакций для отображения')

    args = parser.parse_args()

    # Формируем путь к файлу в папке data
    file_path = os.path.join("data", args.file)

    print(f"📂 Загрузка транзакций из файла: {file_path}")
    print("=" * 60)

    # Используем универсальную функцию для чтения
    transactions = read_transactions(file_path)

    if not transactions:
        print("❌ Не удалось загрузить транзакции. Проверьте файл.")
        print(f"   Искали в: {os.path.abspath(file_path)}")
        return

    print(f"✅ Загружено транзакций: {len(transactions)}")
    print("=" * 60)

    # Тестирование маскирования
    print("\n🔐 Тестирование маскирования:")
    test_card = "1234567890123456"
    masked_card = get_mask_card_number(test_card)
    print(f"  Карта: {masked_card}")

    test_account = "40817810099910004312"
    masked_account = get_mask_account(test_account)
    print(f"  Счет: {masked_account}")
    print("=" * 60)

    # Определяем формат файла для информации
    file_ext = os.path.splitext(file_path)[1].lower()
    print(f"📊 Формат файла: {file_ext}")

    # Обрабатываем транзакции
    limit = min(args.limit, len(transactions))
    for i in range(limit):
        print_transaction_details(transactions[i], i + 1)

    print("\n" + "=" * 60)
    print("✅ Обработка завершена")
    print("📁 Проверь папку 'logs' - там должны быть файлы логов")


if __name__ == "__main__":
    main()
