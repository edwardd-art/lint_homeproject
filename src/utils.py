import json
import os
import re  # Добавляем импорт re для регулярных выражений
from collections import Counter  # Добавляем Counter для подсчета категорий
from typing import Any, Dict, List, cast

import pandas as pd

from src.logger_config import setup_module_logger

logger = setup_module_logger('utils')


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.
    """
    try:
        logger.info(f"Начало чтения JSON-файла: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            print(f"Файл {file_path} не найден")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл {file_path} пустой")
            print(f"Файл {file_path} пустой")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Файл успешно прочитан, получен тип данных: {type(data)}")

        if not isinstance(data, list):
            logger.error(f"Файл {file_path} должен содержать список, получен тип {type(data)}")
            print(f"Файл {file_path} должен содержать список")
            return []

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


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл и возвращает список транзакций.
    """
    try:
        logger.info(f"Начало чтения CSV-файла: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            return []

        df = pd.read_csv(file_path)
        logger.info(f"CSV файл прочитан. Всего записей: {len(df)}")

        transactions = cast(List[Dict[str, Any]], df.to_dict(orient='records'))

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error(f"CSV файл {file_path} пустой")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл и возвращает список транзакций.
    """
    try:
        logger.info(f"Начало чтения Excel-файла: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            return []

        df = pd.read_excel(file_path)
        logger.info(f"Excel файл прочитан. Всего записей: {len(df)}")

        transactions = cast(List[Dict[str, Any]], df.to_dict(orient='records'))

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error(f"Excel файл {file_path} пустой")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel: {e}")
        return []


def read_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения транзакций из разных форматов.
    """
    logger.info(f"Определение формата файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не найден")
        return []

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.json':
        return read_json_file(file_path)
    elif file_extension == '.csv':
        return read_csv_file(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        return read_excel_file(file_path)
    else:
        logger.error(f"Неподдерживаемый формат файла: {file_extension}")
        return []


def convert_amount_to_rub(transaction: Dict[str, Any]) -> float | None:
    """
    Конвертирует сумму транзакции в рубли.
    Временная заглушка для совместимости.
    """
    try:
        logger.info("Конвертация транзакции в рубли (заглушка)")
        return 0.0
    except Exception as e:
        logger.error(f"Ошибка конвертации: {e}")
        return None


# ========== НОВЫЕ ФУНКЦИИ ДЛЯ ЗАДАНИЯ ==========

def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска в описании

    Returns:
        Список транзакций, содержащих строку поиска в описании
    """
    if not transactions:
        logger.info("Пустой список транзакций для поиска")
        return []

    if not search_string:
        logger.warning("Пустая строка поиска")
        return transactions

    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        result = [
            t for t in transactions
            if pattern.search(str(t.get('description', '')))
        ]
        logger.info(f"Найдено {len(result)} транзакций по запросу '{search_string}'")
        return result
    except re.error as e:
        logger.error(f"Ошибка регулярного выражения: {e}")
        return []


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по категориям.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством транзакций по каждой категории
    """
    if not transactions:
        logger.info("Пустой список транзакций для подсчета")
        return {category: 0 for category in categories}

    if not categories:
        logger.warning("Пустой список категорий")
        return {}

    try:
        category_counter = Counter()
        for transaction in transactions:
            description = str(transaction.get('description', ''))
            for category in categories:
                if category.lower() in description.lower():
                    category_counter[category] += 1
                    break

        result = dict(category_counter)
        for category in categories:
            if category not in result:
                result[category] = 0

        logger.info(f"Подсчитаны категории: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при подсчете категорий: {e}")
        return {category: 0 for category in categories}