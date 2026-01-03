import pytest
import os
from unittest.mock import patch, Mock, MagicMock
from src.external_api import ExchangeRateAPI, convert_amount_to_rub


# Фикстура для API ключа
@pytest.fixture(autouse=True)
def set_api_key():
    os.environ["API_KEY"] = "test_key"
    yield


# Исправленный тест с patch декоратором
@patch('src.external_api.requests.get')
def test_patch_decorator_demo(mock_get):
    """Демонстрация использования декоратора @patch"""
    # Настраиваем мок
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 75.5}}
    mock_get.return_value = mock_response

    # Вызываем тестируемую функцию
    api = ExchangeRateAPI()
    result = api.get_exchange_rate("USD")

    # Проверяем результат
    assert result == 75.5

    # Проверяем что мок был вызван с правильными параметрами
    mock_get.assert_called_once()

    # ИЛИ просто проверяем что был вызов (упрощённо)
    assert mock_get.called


# Исправленный тест с side_effect
@patch('src.external_api.requests.get')
def test_mock_side_effect_exception(mock_get):
    """Демонстрация side_effect для исключений"""
    # Настраиваем side_effect для вызова исключения
    mock_get.side_effect = ConnectionError("Нет соединения с интернетом")

    api = ExchangeRateAPI()
    result = api.get_exchange_rate("USD")

    # Функция должна вернуть None при ошибке
    assert result is None
    # Проверяем что функция попыталась сделать запрос
    mock_get.assert_called_once()


# Исправленный тест с patch.object
def test_patch_object_demo():
    """Демонстрация использования patch.object"""
    # Создаем реальный объект
    api = ExchangeRateAPI()

    # Патчим метод get_exchange_rate у КЛАССА ExchangeRateAPI
    with patch.object(ExchangeRateAPI, 'get_exchange_rate') as mock_method:
        mock_method.return_value = 100.0

        # Вызываем метод
        result = api.get_exchange_rate("USD")

        assert result == 100.0
        mock_method.assert_called_once_with("USD", "RUB")
# Альтернативный тест patch.object - правильный


def test_patch_object_correct():
    """Правильное использование patch.object"""
    os.environ["API_KEY"] = "test_key"

    with patch.object(ExchangeRateAPI, 'get_exchange_rate') as mock_method:
        mock_method.return_value = 50.0

        # Теперь ВСЕ объекты ExchangeRateAPI будут использовать мок
        api = ExchangeRateAPI()
        result = api.get_exchange_rate("EUR")

        assert result == 50.0
        mock_method.assert_called_once_with("EUR", "RUB")


# Демонстрация создания мок-объекта
def test_mock_demonstration():
    """Демонстрация создания мок-объекта"""
    # Создаем мок-объект
    mock_response = Mock()

    # Настраиваем его поведение
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.5}}

    # Проверяем настройки
    assert mock_response.status_code == 200
    assert mock_response.json() == {"rates": {"RUB": 75.5}}

    # Проверяем что метод был вызван
    mock_response.json.assert_called_once()


# Демонстрация patch как контекстного менеджера
def test_patch_context_manager():
    """Демонстрация использования patch как контекстного менеджера"""
    os.environ["API_KEY"] = "test_key"

    with patch('src.external_api.requests.get') as mock_get:
        # Настраиваем мок внутри контекстного менеджера
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 80.0}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Тестируемый код
        api = ExchangeRateAPI()
        result = api.get_exchange_rate("EUR")

        # Проверки
        assert result == 80.0
        assert mock_get.called


# Демонстрация side_effect с последовательностью
@patch('src.external_api.requests.get')
def test_mock_side_effect_sequence(mock_get):
    """Демонстрация side_effect с последовательностью значений"""
    os.environ["API_KEY"] = "test_key"

    # Создаем последовательность мок-ответов
    mock_responses = []
    for i in range(3):
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 75.0 + i}}
        mock_responses.append(mock_response)

    mock_get.side_effect = mock_responses

    api = ExchangeRateAPI()

    # Три вызова
    results = []
    for i in range(3):
        result = api.get_exchange_rate("USD")
        results.append(result)

    assert results == [75.0, 76.0, 77.0]
    assert mock_get.call_count == 3


# Простые тесты которые точно работают
def test_convert_rub_simple():
    """Простой тест конвертации рублей"""
    transaction = {"amount": "1000", "currency": "RUB"}
    result = convert_amount_to_rub(transaction)
    assert result == 1000.0


def test_convert_invalid_amount_simple():
    """Простой тест с некорректной суммой"""
    transaction = {"amount": "abc", "currency": "RUB"}
    result = convert_amount_to_rub(transaction)
    assert result is None


# Тест convert_amount_to_rub с моками - ПРАВИЛЬНЫЙ ВАРИАНТ
@patch('src.external_api.ExchangeRateAPI')
def test_convert_usd_with_mocks(MockExchangeRateAPI):
    """Тест конвертации USD с моками"""
    # Настраиваем mock класса
    mock_api_instance = Mock()
    mock_api_instance.get_exchange_rate.return_value = 75.50
    MockExchangeRateAPI.return_value = mock_api_instance

    # Тестируем
    transaction = {"amount": "100.00", "currency": "USD"}
    result = convert_amount_to_rub(transaction)

    assert result == 7550.00
    MockExchangeRateAPI.assert_called_once()
    mock_api_instance.get_exchange_rate.assert_called_once_with("USD", "RUB")