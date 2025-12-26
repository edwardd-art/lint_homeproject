import json
import os
from typing import List, Dict, Any


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
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные - список
        if not isinstance(data, list):
            return []

        return data

    except json.JSONDecodeError:
        return []
    except Exception:
        return []