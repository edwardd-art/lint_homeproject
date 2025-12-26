import pytest
from unittest.mock import Mock, patch
from src.external_api import convert_amount_to_rub


# Только самые важные тесты
def test_convert_rub_simple():
    """Простой тест рублей"""
    result = convert_amount_to_rub({"amount": "100", "currency": "RUB"})
    assert result == 100.0


# Создайте отдельный тестовый файл с этим