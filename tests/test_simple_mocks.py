"""Простые тесты для демонстрации mock и patch"""
import pytest
from unittest.mock import Mock, patch
from src.external_api import convert_amount_to_rub


# Пример 1: Простой Mock
def test_simple_mock():
    """Самый простой пример Mock"""
    mock_calculator = Mock()
    mock_calculator.add.return_value = 5

    result = mock_calculator.add(2, 3)

    assert result == 5
    mock_calculator.add.assert_called_once_with(2, 3)


# Пример 2: @patch декоратор
@patch('src.external_api.ExchangeRateAPI')
def test_convert_with_patch_decorator(MockAPI):
    """Пример с @patch декоратором"""
    mock_instance = Mock()
    mock_instance.get_exchange_rate.return_value = 70.0
    MockAPI.return_value = mock_instance

    result = convert_amount_to_rub({"amount": "100", "currency": "USD"})

    assert result == 7000.0
    MockAPI.assert_called_once()


# Пример 3: patch как контекстный менеджер
def test_convert_with_patch_context():
    """Пример с patch как контекстный менеджер"""
    with patch('src.external_api.ExchangeRateAPI') as MockAPI:
        mock_instance = Mock()
        mock_instance.get_exchange_rate.return_value = 80.0
        MockAPI.return_value = mock_instance

        result = convert_amount_to_rub({"amount": "50", "currency": "EUR"})

        assert result == 4000.0


# Пример 4: side_effect
def test_mock_with_side_effect():
    """Пример с side_effect"""
    mock_func = Mock()
    mock_func.side_effect = [1, 2, 3]

    assert mock_func() == 1
    assert mock_func() == 2
    assert mock_func() == 3
    assert mock_func.call_count == 3


# Пример 5: Проверка вызовов
@patch('src.external_api.ExchangeRateAPI')
def test_mock_call_verification(MockAPI):
    """Пример проверки вызовов"""
    mock_instance = Mock()
    mock_instance.get_exchange_rate.return_value = 75.5
    MockAPI.return_value = mock_instance

    # Вызываем два раза
    convert_amount_to_rub({"amount": "100", "currency": "USD"})
    convert_amount_to_rub({"amount": "200", "currency": "USD"})

    # Проверяем что создан один экземпляр
    MockAPI.assert_called_once()

    # Проверяем что метод вызван два раза
    assert mock_instance.get_exchange_rate.call_count == 2

    # Проверяем аргументы первого вызова
    assert mock_instance.get_exchange_rate.call_args_list[0] == pytest.approx((("USD", "RUB"), {}))