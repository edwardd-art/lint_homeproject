"""Тесты для модуля external_api."""
import os
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import ExchangeRateAPI, convert_amount_to_rub


# Фикстура для автоматической установки API ключа
@pytest.fixture(autouse=True)
def setup_env():
    """Автоматическая установка переменных окружения для тестов."""
    os.environ["API_KEY"] = "test_key_123"
    yield
    # Очистка после теста
    if "API_KEY" in os.environ:
        del os.environ["API_KEY"]


# ТЕСТЫ ДЛЯ convert_amount_to_rub
def test_convert_rub():
    """Тест конвертации рублей."""
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "code": "RUB"
            }
        }
    }
    result = convert_amount_to_rub(transaction)
    assert result == 1000.50
    assert isinstance(result, float)


def test_convert_invalid_amount():
    """Тест с некорректной суммой."""
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


def test_convert_missing_operation_amount():
    """Тест без operationAmount."""
    transaction = {"id": 1}
    result = convert_amount_to_rub(transaction)
    assert result is None


def test_convert_missing_amount():
    """Тест без amount."""
    transaction = {
        "operationAmount": {
            "currency": {"code": "RUB"}
        }
    }
    result = convert_amount_to_rub(transaction)
    assert result is None


def test_convert_missing_currency():
    """Тест без currency."""
    transaction = {
        "operationAmount": {
            "amount": "100"
        }
    }
    result = convert_amount_to_rub(transaction)
    assert result is None


def test_convert_missing_currency_code():
    """Тест без code в currency."""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "руб."}
        }
    }
    result = convert_amount_to_rub(transaction)
    assert result is None


# ТЕСТЫ С MOCK И PATCH
@patch('src.external_api.ExchangeRateAPI')
def test_convert_usd_with_mock(MockAPI):
    """Тест конвертации USD с использованием mock и patch."""
    # Настраиваем mock
    mock_instance = Mock()
    mock_instance.convert_currency.return_value = 7500.00
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

    # Проверяем результат
    assert result == 7500.00
    assert isinstance(result, float)

    # Проверяем что mock был использован правильно
    MockAPI.assert_called_once()
    mock_instance.convert_currency.assert_called_once_with(100.00, "USD", "RUB")


@patch('src.external_api.ExchangeRateAPI')
def test_convert_eur_with_mock(MockAPI):
    """Тест конвертации EUR с использованием mock и patch."""
    mock_instance = Mock()
    mock_instance.convert_currency.return_value = 9000.00
    MockAPI.return_value = mock_instance

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "EUR"
            }
        }
    }

    result = convert_amount_to_rub(transaction)

    assert result == 9000.00
    MockAPI.assert_called_once()
    mock_instance.convert_currency.assert_called_once_with(100.00, "EUR", "RUB")


@patch('src.external_api.ExchangeRateAPI')
def test_convert_api_returns_none(MockAPI):
    """Тест когда API возвращает None."""
    mock_instance = Mock()
    mock_instance.convert_currency.return_value = None
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

    assert result is None
    MockAPI.assert_called_once()
    mock_instance.convert_currency.assert_called_once_with(100.00, "USD", "RUB")


# ТЕСТЫ ДЛЯ ExchangeRateAPI
def test_exchange_api_init_no_key():
    """Тест инициализации без ключа."""
    # Сохраняем и удаляем ключ
    original_key = os.environ.get("API_KEY")
    if "API_KEY" in os.environ:
        del os.environ["API_KEY"]

    try:
        with pytest.raises(ValueError, match="API_KEY не найден"):
            ExchangeRateAPI()
    finally:
        # Восстанавливаем ключ
        if original_key:
            os.environ["API_KEY"] = original_key


def test_exchange_api_rub_conversion():
    """Тест что RUB возвращает ту же сумму."""
    api = ExchangeRateAPI()
    result = api.convert_currency(100.0, "RUB")
    assert result == 100.0


@patch('src.external_api.requests.get')
def test_exchange_api_success(mock_get):
    """Тест успешного вызова API."""
    # Настраиваем mock ответ
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "result": 7500.00
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = ExchangeRateAPI()
    result = api.convert_currency(100.0, "USD", "RUB")

    assert result == 7500.00
    mock_get.assert_called_once()


@patch('src.external_api.requests.get')
def test_exchange_api_error(mock_get):
    """Тест ошибки API с использованием mock."""
    # Используем RequestException, которое обрабатывает ваш код
    mock_get.side_effect = requests.exceptions.RequestException("API error")

    api = ExchangeRateAPI()

    # Ваш метод должен вернуть None
    result = api.convert_currency(100.0, "USD", "RUB")

    # Проверяем что вернулось None
    assert result is None

    # Проверяем что requests.get был вызван
    mock_get.assert_called_once()


@patch('src.external_api.requests.get')
def test_exchange_api_no_success(mock_get):
    """Тест когда API возвращает success: false."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": False,
        "error": {"info": "Invalid API key"}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = ExchangeRateAPI()
    result = api.convert_currency(100.0, "USD", "RUB")

    assert result is None
    mock_get.assert_called_once()


# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ДЛЯ ДЕМОНСТРАЦИИ MOCK/PATCH
def test_simple_mock_example():
    """Простой пример использования Mock для проверки знаний."""
    # Создаем mock объект
    mock_calculator = Mock()

    # Настраиваем его поведение
    mock_calculator.add.return_value = 42
    mock_calculator.multiply.return_value = 100

    # Используем mock
    result1 = mock_calculator.add(10, 32)
    result2 = mock_calculator.multiply(10, 10)

    # Проверяем результаты
    assert result1 == 42
    assert result2 == 100

    # Проверяем что методы были вызваны с правильными аргументами
    mock_calculator.add.assert_called_once_with(10, 32)
    mock_calculator.multiply.assert_called_once_with(10, 10)


def test_mock_side_effect_example():
    """Пример использования side_effect."""
    mock_func = Mock()

    # Настраиваем side_effect для возвращения разных значений
    mock_func.side_effect = [1, 2, 3, StopIteration]

    # Первые три вызова возвращают значения
    assert mock_func() == 1
    assert mock_func() == 2
    assert mock_func() == 3

    # Четвертый вызов вызовет StopIteration
    with pytest.raises(StopIteration):
        mock_func()

    assert mock_func.call_count == 4


def test_patch_as_context_manager():
    """Пример использования patch как контекстного менеджера."""
    with patch('src.external_api.ExchangeRateAPI') as MockAPI:
        mock_instance = Mock()
        mock_instance.convert_currency.return_value = 5000.00
        MockAPI.return_value = mock_instance

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }

        result = convert_amount_to_rub(transaction)

        assert result == 5000.00
        MockAPI.assert_called_once()
