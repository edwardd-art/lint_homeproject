"""Тесты для модуля utils."""
import json
import os
import tempfile
from src.utils import read_json_file


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
