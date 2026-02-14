# utils.py
import json
import os
from typing import Any, Dict, List

from logger_config import setup_module_logger

# Создаем логгер для модуля utils
logger = setup_module_logger('utils')


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с транзакциями или пустой список в случае ошибки
    """
    try:
        logger.info(f"Начало чтения JSON-файла: {file_path}")

        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            print(f"Файл {file_path} не найден")
            return []

        # Проверяем, не пустой ли файл
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл {file_path} пустой")
            print(f"Файл {file_path} пустой")
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Файл успешно прочитан, получен тип данных: {type(data)}")

        # Проверяем, что данные - список
        if not isinstance(data, list):
            logger.error(f"Файл {file_path} должен содержать список, получен тип {type(data)}")
            print(f"Файл {file_path} должен содержать список")
            return []

        # Фильтруем пустые словари (если есть)
        valid_transactions = [item for item in data if isinstance(item, dict) and item]
        logger.info(f"Найдено {len(valid_transactions)} валидных транзакций из {len(data)} записей")
        print(f"Найдено транзакций: {len(valid_transactions)}")

        return valid_transactions

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден (FileNotFoundError)")
        print(f"Файл {file_path} не найден (FileNotFoundError)")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
