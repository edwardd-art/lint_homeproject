"""Основной скрипт для работы с реальными данными"""

import os
from typing import Any, Dict, List, Optional

from src.mask import get_mask_account, get_mask_card_number
from src.utils import (
    read_transactions,
    search_transactions,
    count_transactions_by_category
)


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
            if len(number) == 16:
                masked_number = get_mask_card_number(number)
                from_field = ' '.join(words[:-1] + [masked_number])
                print(f"  Откуда: {from_field}")
            elif len(number) > 16:
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
            if len(number) == 16:
                masked_number = get_mask_card_number(number)
                to_field = ' '.join(words[:-1] + [masked_number])
                print(f"  Куда: {to_field}")
            elif len(number) > 16:
                masked_number = get_mask_account(number)
                to_field = ' '.join(words[:-1] + [masked_number])
                print(f"  Куда: {to_field}")
        else:
            print(f"  Куда: {to_field}")
    else:
        print("  Куда: Не указано")

    amount = transaction.get('amount', transaction.get('Сумма', 'N/A'))
    currency = transaction.get('currency', transaction.get('Валюта', 'RUB'))

    print(f"  Сумма: {amount} {currency}")


def filter_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу (без учета регистра)"""
    return [t for t in transactions if t.get('state', '').lower() == status.lower()]


def sort_by_date(transactions: List[Dict[str, Any]], ascending: bool = True) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате"""
    return sorted(
        transactions,
        key=lambda x: x.get('date', ''),
        reverse=not ascending
    )


def filter_rub_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует только рублевые транзакции"""
    return [t for t in transactions if t.get('currency') == 'RUB']


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Получает выбор пользователя из списка вариантов"""
    while True:
        choice = input(prompt).strip()
        if choice.lower() in [opt.lower() for opt in options]:
            return choice
        print(f"Некорректный ввод. Доступные варианты: {', '.join(options)}")


def get_yes_no(prompt: str) -> bool:
    """Получает ответ Да/Нет от пользователя"""
    while True:
        choice = input(prompt + " (да/нет): ").strip().lower()
        if choice in ['да', 'yes', 'y', 'д']:
            return True
        if choice in ['нет', 'no', 'n']:
            return False
        print("Пожалуйста, ответьте 'да' или 'нет'")


def main() -> None:
    """Главная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор источника данных
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = get_user_choice("Ваш выбор: ", ["1", "2", "3"])

    file_map = {
        "1": ("operations.json", "JSON"),
        "2": ("transactions.csv", "CSV"),
        "3": ("transactions_excel.xlsx", "XLSX")
    }

    file_name, file_type = file_map[file_choice]
    file_path = os.path.join("data", file_name)

    print(f"\nДля обработки выбран {file_type}-файл.")

    # Загрузка транзакций
    transactions = read_transactions(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте наличие файла.")
        return

    # Фильтрация по статусу
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    filtered_transactions = None

    while True:
        status_input = input(
            f"\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные статусы: {', '.join(available_statuses)}\n"
        ).strip()

        if status_input.upper() in [s.upper() for s in available_statuses]:
            filtered_transactions = filter_by_status(transactions, status_input)
            print(f"Операции отфильтрованы по статусу \"{status_input.upper()}\"")
            break
        else:
            print(f"Статус операции \"{status_input}\" недоступен.")

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    transactions_to_process = filtered_transactions

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате?"):
        order = get_user_choice("Отсортировать по возрастанию или по убыванию? ", ["по возрастанию", "по убыванию"])
        ascending = order.lower() == "по возрастанию"
        transactions_to_process = sort_by_date(transactions_to_process, ascending)
        print(f"Операции отсортированы по дате ({order})")

    # Фильтрация по рублевым транзакциям
    if get_yes_no("\nВыводить только рублевые транзакции?"):
        transactions_to_process = filter_rub_transactions(transactions_to_process)
        if not transactions_to_process:
            print("\nНе найдено ни одной рублевой транзакции, подходящей под ваши условия фильтрации")
            return

    # Поиск по описанию
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            transactions_to_process = search_transactions(transactions_to_process, search_word)
            if not transactions_to_process:
                print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
                return

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions_to_process)}")

    for i, transaction in enumerate(transactions_to_process, 1):
        print_transaction_details(transaction, i)

    # Подсчет по категориям
    categories = ["Перевод", "Оплата", "Покупка", "Снятие"]
    category_counts = count_transactions_by_category(transactions_to_process, categories)

    if category_counts and any(count > 0 for count in category_counts.values()):
        print("\n📊 Статистика по категориям:")
        for category, count in category_counts.items():
            if count > 0:
                print(f"  {category}: {count} операций")
    else:
        print("\n📊 Нет операций для подсчета статистики по категориям")


if __name__ == "__main__":
    main()