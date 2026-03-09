"""Тесты для модуля utils."""
import json
import os
import tempfile
import pandas as pd
import pytest
from src.utils import (
    read_json_file,
    read_csv_file,
    read_excel_file,
    read_transactions
)


# ====== Существующие тесты для JSON ======
def test_read_json_file_success():
    """Тест успешного чтения файла."""
    test_data = [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}},
        {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "USD"}}}
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        result = read_json_file(temp_file)
        assert result == test_data
    finally:
        os.unlink(temp_file)


def test_read_json_file_not_found():
    """Тест когда файл не найден."""
    result = read_json_file("/non/existent/file.json")
    assert result == []


def test_read_json_file_empty():
    """Тест пустого файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    try:
        result = read_json_file(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_read_json_file_invalid_json():
    """Тест с некорректным JSON."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{invalid json")
        temp_file = f.name

    try:
        result = read_json_file(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_read_json_file_not_list():
    """Тест когда файл содержит не список."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"key": "value"}, f)
        temp_file = f.name

    try:
        result = read_json_file(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_read_json_file_empty_dicts():
    """Тест с пустыми словарями в списке."""
    test_data = [{}, {"id": 1}, {}]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        result = read_json_file(temp_file)
        # Должен вернуть только непустые словари
        assert result == [{"id": 1}]
    finally:
        os.unlink(temp_file)


# ====== Новые тесты для CSV ======
def test_read_csv_file_success():
    """Тест успешного чтения CSV файла."""
    # Создаем временный CSV файл
    csv_content = "id,amount,currency\n1,1000,RUB\n2,500,USD\n3,750,EUR"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    try:
        result = read_csv_file(temp_file)

        # Проверяем результат
        assert len(result) == 3
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 1000
        assert result[0]['currency'] == 'RUB'
        assert result[1]['currency'] == 'USD'
        assert result[2]['currency'] == 'EUR'
    finally:
        os.unlink(temp_file)


def test_read_csv_file_not_found():
    """Тест отсутствующего CSV файла."""
    result = read_csv_file("non_existent_file.csv")
    assert result == []


def test_read_csv_file_empty():
    """Тест пустого CSV файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_file = f.name

    try:
        result = read_csv_file(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_read_csv_file_with_headers():
    """Тест CSV файла с разными заголовками."""
    csv_content = "transaction_id,sum,currency_code\n101,1500,RUB\n102,2500,USD"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    try:
        result = read_csv_file(temp_file)

        assert len(result) == 2
        assert result[0]['transaction_id'] == 101
        assert result[0]['sum'] == 1500
        assert result[0]['currency_code'] == 'RUB'
    finally:
        os.unlink(temp_file)


def test_read_csv_file_malformed():
    """Тест поврежденного CSV файла."""
    csv_content = "id,amount\n1,1000\n2,500,extra\n3,700"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    try:
        # Должен вернуть пустой список при ошибке парсинга
        result = read_csv_file(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


# ====== Новые тесты для Excel ======
def test_read_excel_file_success():
    """Тест успешного чтения Excel файла."""
    # Создаем временный Excel файл
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        temp_file = tmp.name

    try:
        # Создаем DataFrame и сохраняем в Excel
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'amount': [1000, 500, 750],
            'currency': ['RUB', 'USD', 'EUR']
        })
        df.to_excel(temp_file, index=False)

        # Тестируем функцию
        result = read_excel_file(temp_file)

        assert len(result) == 3
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 1000
        assert result[0]['currency'] == 'RUB'
        assert result[1]['currency'] == 'USD'
        assert result[2]['currency'] == 'EUR'
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_read_excel_file_not_found():
    """Тест отсутствующего Excel файла."""
    result = read_excel_file("non_existent_file.xlsx")
    assert result == []


def test_read_excel_file_empty():
    """Тест пустого Excel файла (создать пустой Excel сложно, проверим только отсутствие)."""
    # Создаем временный файл, но не пишем в него данные
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        temp_file = tmp.name

    try:
        # Это должно вызвать ошибку EmptyDataError
        result = read_excel_file(temp_file)
        assert result == []
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_read_excel_file_with_different_sheet():
    """Тест Excel файла с указанием листа (по умолчанию берется первый)."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        temp_file = tmp.name

    try:
        # Создаем Excel с несколькими листами
        with pd.ExcelWriter(temp_file) as writer:
            df1 = pd.DataFrame({'id': [1, 2], 'amount': [1000, 500]})
            df2 = pd.DataFrame({'id': [3, 4], 'amount': [750, 250]})
            df1.to_excel(writer, sheet_name='Sheet1', index=False)
            df2.to_excel(writer, sheet_name='Sheet2', index=False)

        # Должен прочитать Sheet1 (первый)
        result = read_excel_file(temp_file)

        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 1000
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


# ====== Тесты для универсальной функции read_transactions ======
def test_read_transactions_json():
    """Тест универсальной функции с JSON файлом."""
    test_data = [{"id": 1, "amount": 1000}]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        result = read_transactions(temp_file)
        assert len(result) == 1
        assert result[0]['id'] == 1
    finally:
        os.unlink(temp_file)


def test_read_transactions_csv():
    """Тест универсальной функции с CSV файлом."""
    csv_content = "id,amount\n1,1000\n2,500"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    try:
        result = read_transactions(temp_file)
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 1000
    finally:
        os.unlink(temp_file)


def test_read_transactions_excel():
    """Тест универсальной функции с Excel файлом."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        temp_file = tmp.name

    try:
        df = pd.DataFrame({'id': [1, 2], 'amount': [1000, 500]})
        df.to_excel(temp_file, index=False)

        result = read_transactions(temp_file)
        assert len(result) == 2
        assert result[0]['id'] == 1
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_read_transactions_unsupported_format():
    """Тест универсальной функции с неподдерживаемым форматом."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b"some data")
        temp_file = f.name

    try:
        result = read_transactions(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_read_transactions_not_found():
    """Тест универсальной функции с несуществующим файлом."""
    result = read_transactions("non_existent.xyz")
    assert result == []