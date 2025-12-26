#!/usr/bin/env python3
"""Основной файл для тестирования проекта"""

import os
from src import read_json_file, convert_amount_to_rub


def main():
    # Читаем транзакции
    file_path = os.path.join("data", "operations.json")
    transactions = read_json_file(file_path)
    
    print(f"Загружено транзакций: {len(transactions)}")
    print("=" * 50)
    
    # Конвертируем каждую транзакцию
    total_rub = 0.0
    
    for i, transaction in enumerate(transactions, 1):
        amount_rub = convert_amount_to_rub(transaction)
        
        if amount_rub is not None:
            print(f"Транзакция #{transaction.get('id', i)}")
            print(f"  Описание: {transaction.get('description', 'N/A')}")
            print(f"  Сумма: {transaction.get('amount')} {transaction.get('currency')}")
            print(f"  В рублях: {amount_rub:.2f} RUB")
            total_rub += amount_rub
        else:
            print(f"Транзакция #{i}: Ошибка конвертации")
        
        print("-" * 30)
    
    print(f"\nОбщая сумма в рублях: {total_rub:.2f} RUB")
    
    # Проверка API ключа
    api_key = os.getenv("API_KEY")
    if api_key and api_key != "your_api_key_here":
        print(f"\n✅ API ключ загружен (первые 5 символов: {api_key[:5]}...)")
    else:
        print("\n⚠️  Проверьте файл .env")


if __name__ == "__main__":
    main()
