import json
import os
import re
from collections import Counter
from typing import Any, Dict, List, cast

import pandas as pd

from logger_config import setup_module_logger

logger = setup_module_logger('utils')


def normalize_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Приводит транзакции из разных форматов (JSON, CSV, Excel) к единому виду.

    Args:
        transaction: Сырая транзакция из файла

    Returns:
        Нормализованная транзакция с единой структурой
    """
    normalized = {}

    # Базовые поля
    normalized['id'] = transaction.get('id')
    normalized['state'] = transaction.get('state', '')
    normalized['date'] = transaction.get('date', '')
    normalized['description'] = transaction.get('description', '')
    normalized['from'] = transaction.get('from', '')
    normalized['to'] = transaction.get('to', '')

    # Универсальное получение суммы и валюты
    # Проверяем, есть ли вложенная структура operationAmount (как в JSON)
    if 'operationAmount' in transaction and isinstance(transaction['operationAmount'], dict):
        # JSON формат
        op_amount = transaction['operationAmount']
        normalized['amount'] = op_amount.get('amount', '')
        if 'currency' in op_amount and isinstance(op_amount['currency'], dict):
            normalized['currency'] = op_amount['currency'].get('code', '')
            normalized['currency_name'] = op_amount['currency'].get('name', '')
        else:
            normalized['currency'] = ''
            normalized['currency_name'] = ''
    else:
        # CSV/Excel формат
        normalized['amount'] = transaction.get('amount', transaction.get('Сумма', ''))
        normalized['currency'] = transaction.get('currency', transaction.get('currency_code', ''))
        normalized['currency_name'] = transaction.get('currency_name', transaction.get('Валюта', ''))

    return normalized


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список нормализованных транзакций.
    """
    try:
        logger.info(f"Начало чтения JSON-файла: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл {file_path} пустой")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.error(f"Файл {file_path} должен содержать список")
            return []

        valid_transactions = [item for item in data if isinstance(item, dict) and item]

        # Нормализуем каждую транзакцию
        normalized_transactions = [normalize_transaction(t) for t in valid_transactions]

        logger.info(f"Найдено {len(normalized_transactions)} валидных транзакций")
        return normalized_transactions

    except Exception as e:
        logger.error(f"Ошибка при чтении JSON: {e}")
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл и возвращает список нормализованных транзакций.
    """
    try:
        logger.info(f"Начало чтения CSV-файла: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            return []

        # Пробуем разные разделители
        separators = [',', ';', '\t', '|']
        df = None

        for sep in separators:
            try:
                df = pd.read_csv(file_path, sep=sep, encoding='utf-8')
                if len(df.columns) > 1:
                    break
            except:
                continue

        if df is None or len(df.columns) == 1:
            # Если не удалось определить разделитель, читаем с автоопределением
            df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')

        logger.info(f"CSV файл прочитан. Всего записей: {len(df)}")

        # Приводим названия колонок к единому формату (нижний регистр)
        df.columns = [col.lower().strip() for col in df.columns]

        transactions = cast(List[Dict[str, Any]], df.to_dict(orient='records'))

        # Нормализуем каждую транзакцию
        normalized_transactions = [normalize_transaction(t) for t in transactions]

        logger.info(f"Успешно загружено {len(normalized_transactions)} транзакций из CSV")
        return normalized_transactions

    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл и возвращает список нормализованных транзакций.
    """
    try:
        logger.info(f"Начало чтения Excel-файла: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            return []

        df = pd.read_excel(file_path)
        logger.info(f"Excel файл прочитан. Всего записей: {len(df)}")

        # Приводим названия колонок к единому формату (нижний регистр)
        df.columns = [col.lower().strip() for col in df.columns]

        transactions = cast(List[Dict[str, Any]], df.to_dict(orient='records'))

        # Нормализуем каждую транзакцию
        normalized_transactions = [normalize_transaction(t) for t in transactions]

        logger.info(f"Успешно загружено {len(normalized_transactions)} транзакций из Excel")
        return normalized_transactions

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


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.
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