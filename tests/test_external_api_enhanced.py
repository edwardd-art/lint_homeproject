import pytest
import os
from unittest.mock import patch, Mock
from src.external_api import ExchangeRateAPI, convert_amount_to_rub


# Фикстура для API ключа
@pytest.fixture(autouse=True)
def set_api_key():
    os.environ["API_KEY"] = "test_key"
    yield


def test_convert_amount_to_rub_returns_float():
    """Тест что функция всегда возвращает float или None"""
    # Тест для RUB
    transaction = {"amount": "100.50", "currency": "RUB"}
    result = convert_amount_to_rub(transaction)
    assert isinstance(result, float)
    assert result == 100.50


def test_convert_amount_to_rub_invalid_amount():
    """Тест с некорректной суммой"""
    transaction = {"amount": "not_a_number", "currency": "RUB"}
    result = convert_amount_to_rub(transaction)
    assert result is None


def test_convert_amount_to_rub_missing_fields():
    """Тест с отсутствующими полями"""
    # Без amount
    transaction1 = {"currency": "RUB"}
    result1 = convert_amount_to_rub(transaction1)
    assert result1 is None

    # Без currency
    transaction2 = {"amount": "100"}
    result2 = convert_amount_to_rub(transaction2)
    assert result2 is None


# ПРАВИЛЬНЫЙ тест с API
@patch('src.external_api.ExchangeRateAPI')
def test_convert_amount_to_rub_with_api(MockExchangeRateAPI):
    """Тест конвертации с использованием API"""
    # Настраиваем mock экземпляра
    mock_api_instance = Mock()
    mock_api_instance.get_exchange_rate.return_value = 75.50

    # Настраиваем КЛАСС чтобы возвращал наш mock экземпляр
    MockExchangeRateAPI.return_value = mock_api_instance

    transaction = {"amount": "100.00", "currency": "USD"}
    result = convert_amount_to_rub(transaction)

    # Проверяем что результат - float
    assert isinstance(result, float)
    assert result == 7550.00

    # Проверяем что КЛАСС был вызван
    MockExchangeRateAPI.assert_called_once()

    # Проверяем что метод у ЭКЗЕМПЛЯРА был вызван
    mock_api_instance.get_exchange_rate.assert_called_once()

    # Проверяем с какими аргументами был вызван
    mock_api_instance.get_exchange_rate.assert_called_once_with("USD", "RUB")


def test_exchange_rate_api_returns_float():
    """Тест что API всегда возвращает float или None"""
    with patch('src.external_api.requests.get') as mock_get:
        # Настраиваем успешный ответ
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 75.50}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = ExchangeRateAPI()
        result = api.get_exchange_rate("USD")

        # Проверяем что результат - float
        assert isinstance(result, float)
        assert result == 75.50


def test_exchange_rate_api_rub_returns_float():
    """Тест что для RUB возвращается 1.0 как float"""
    api = ExchangeRateAPI()
    result = api.get_exchange_rate("RUB")

    assert isinstance(result, float)
    assert result == 1.0


def test_convert_unsupported_currency():
    """Тест конвертации неподдерживаемой валюты"""
    transaction = {"amount": "100.00", "currency": "ABC"}
    result = convert_amount_to_rub(transaction)
    assert result is None


# Упрощенный тест для демонстрации
def test_simple_mock_example():
    """Простой пример использования mock"""
    # Создаем mock объект
    mock_obj = Mock()

    # Настраиваем его поведение
    mock_obj.calculate.return_value = 42

    # Используем
    result = mock_obj.calculate(10, 20)

    # Проверяем
    assert result == 42
    mock_obj.calculate.assert_called_once_with(10, 20)