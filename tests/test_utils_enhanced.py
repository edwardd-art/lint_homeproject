import pytest
import json
import os
from src.utils import read_json_file


def test_read_json_file_file_not_found():
    """Тест обработки FileNotFoundError"""
    result = read_json_file("/non/existent/path/file.json")
    assert result == []


def test_read_json_file_empty_file(tmp_path):
    """Тест обработки пустого файла"""
    file_path = tmp_path / "empty.json"
    file_path.touch()  # Создаем пустой файл

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_not_json(tmp_path):
    """Тест обработки файла не в формате JSON"""
    file_path = tmp_path / "not_json.txt"
    with open(file_path, 'w') as f:
        f.write("Это не JSON файл")

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_not_list(tmp_path):
    """Тест обработки файла с JSON но не списком"""
    file_path = tmp_path / "not_list.json"
    with open(file_path, 'w') as f:
        json.dump({"key": "value"}, f)

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_success(tmp_path):
    """Тест успешного чтения файла"""
    test_data = [
        {"id": 1, "amount": "100.50", "currency": "USD"},
        {"id": 2, "amount": "200.00", "currency": "RUB"}
    ]

    file_path = tmp_path / "test.json"
    with open(file_path, 'w') as f:
        json.dump(test_data, f)

    result = read_json_file(str(file_path))
    assert result == test_data