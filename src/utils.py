import json
import os
from typing import Any, Dict, List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с транзакциями или пустой список в случае ошибки
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден")
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            print(f"Файл {file_path} пустой")
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - список
        if not isinstance(data, list):
            print(f"Файл {file_path} должен содержать список")
            return []

        # Фильтруем пустые словари (если есть)
        valid_transactions = [item for item in data if isinstance(item, dict) and item]

        return valid_transactions

    except FileNotFoundError:
        print(f"Файл {file_path} не найден (FileNotFoundError)")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
