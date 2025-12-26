import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.utils import read_json_file


def test_read_json_file_success(tmp_path):
    """Тест успешного чтения JSON файла"""
    # Создаем тестовый JSON файл
    test_data = [
        {"id": 1, "amount": "100.50", "currency": "USD"},
        {"id": 2, "amount": "200.00", "currency": "RUB"}
    ]

    file_path = tmp_path / "test.json"
    with open(file_path, 'w') as f:
        json.dump(test_data, f)

    result = read_json_file(str(file_path))
    assert result == test_data


def test_read_json_file_not_found():
    """Тест на несуществующий файл"""
    result = read_json_file("/non/existent/file.json")
    assert result == []


def test_read_json_file_empty(tmp_path):
    """Тест на пустой файл"""
    file_path = tmp_path / "empty.json"
    file_path.touch()

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_not_list(tmp_path):
    """Тест на файл с не списком"""
    file_path = tmp_path / "not_list.json"
    with open(file_path, 'w') as f:
        json.dump({"key": "value"}, f)

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_invalid_json(tmp_path):
    """Тест на некорректный JSON"""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w') as f:
        f.write("{invalid json")

    result = read_json_file(str(file_path))
    assert result == []