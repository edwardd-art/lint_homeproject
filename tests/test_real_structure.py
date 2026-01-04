"""Тесты для проверки работы с реальной структурой данных"""
import pytest
import json
import tempfile
import os
from unittest.mock import patch, Mock
from src.utils import read_json_file
from src.external_api import convert_amount_to_rub


def test_read_real_structure():
    """Тест чтения транзакции с реальной структурой"""
    # Создаем транзакцию с реальной структурой
    real_transaction = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }

    # Создаем временный файл с такой структурой
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([real_transaction], f)
        temp_file = f.name

    try:
        # Читаем файл
        transactions = read_json_file(temp_file)

        assert len(transactions) == 1
        transaction = transactions[0]

        # Проверяем структуру
        assert "operationAmount" in transaction
        assert "amount" in transaction["operationAmount"]
        assert "currency" in transaction["operationAmount"]
        assert "code" in transaction["operationAmount"]["currency"]

    finally:
        os.unlink(temp_file)


def test_convert_rub_real_structure():
    """Тест конвертации RUB с реальной структурой"""
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    }

    result = convert_amount_to_rub(transaction)

    assert result == 1000.50
    assert isinstance(result, float)


def test_convert_usd_real_structure():
    """Тест конвертации USD с реальной структурой"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }

    # Мокаем API
    with patch('src.external_api.ExchangeRateAPI') as MockAPI:
        mock_instance = Mock()
        mock_instance.convert_currency.return_value = 7500.00
        MockAPI.return_value = mock_instance

        result = convert_amount_to_rub(transaction)

        assert result == 7500.00
        assert isinstance(result, float)

        # Проверяем что API было вызвано с правильными параметрами
        mock_instance.convert_currency.assert_called_once_with(100.00, "USD", "RUB")


def test_missing_fields():
    """Тест с отсутствующими полями в реальной структуре"""
    # Без operationAmount
    transaction1 = {"id": 1}
    result1 = convert_amount_to_rub(transaction1)
    assert result1 is None

    # Без amount
    transaction2 = {
        "operationAmount": {
            "currency": {"code": "RUB"}
        }
    }
    result2 = convert_amount_to_rub(transaction2)
    assert result2 is None

    # Без currency
    transaction3 = {
        "operationAmount": {
            "amount": "100"
        }
    }
    result3 = convert_amount_to_rub(transaction3)
    assert result3 is None

    # Без code в currency
    transaction4 = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "руб."}
        }
    }
    result4 = convert_amount_to_rub(transaction4)
    assert result4 is None


def test_invalid_amount():
    """Тест с некорректной суммой"""
    transaction = {
        "operationAmount": {
            "amount": "not_a_number",
            "currency": {
                "code": "RUB"
            }
        }
    }

    result = convert_amount_to_rub(transaction)
    assert result is None


# Тест с моками для нового метода convert_currency
@patch('src.external_api.ExchangeRateAPI')
def test_mock_convert_currency(MockAPI):
    """Тест с моком нового метода convert_currency"""
    mock_instance = Mock()
    mock_instance.convert_currency.return_value = 8500.00
    MockAPI.return_value = mock_instance

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    result = convert_amount_to_rub(transaction)

    assert result == 8500.00
    MockAPI.assert_called_once()
    mock_instance.convert_currency.assert_called_once_with(100.00, "USD", "RUB")