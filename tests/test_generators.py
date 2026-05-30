import os
import sys

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Добавляем папку src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"code": "USD"}
            },
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"code": "USD"}
            },
            "description": "Перевод со счета на счет"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"code": "RUB"}
            },
            "description": "Перевод со счета на счет"
        }
    ]


class TestFilterByCurrency:
    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в USD"""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2
        assert all(t['operationAmount']['currency']['code'] == 'USD' for t in usd_transactions)

    def test_filter_rub_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в RUB"""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1
        assert rub_transactions[0]['operationAmount']['currency']['code'] == 'RUB'

    def test_filter_empty_result(self, sample_transactions):
        """Тест фильтрации с пустым результатом"""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0


class TestTransactionDescriptions:
    def test_descriptions_generator(self, sample_transactions):
        """Тест генератора описаний транзакций"""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]
        assert descriptions == expected

    def test_empty_transactions(self):
        """Тест с пустым списком транзакций"""
        descriptions = list(transaction_descriptions([]))
        assert descriptions == []


class TestCardNumberGenerator:
    def test_single_card_number(self):
        """Тест генерации одного номера карты"""
        generator = card_number_generator(1, 1)
        cards = list(generator)
        assert cards == ["0000 0000 0000 0001"]

    def test_card_number_range(self):
        """Тест генерации диапазона номеров карт"""
        generator = card_number_generator(1, 5)
        cards = list(generator)
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005"
        ]
        assert cards == expected

    def test_large_card_numbers(self):
        """Тест генерации больших номеров карт"""
        generator = card_number_generator(9999999999999998, 9999999999999999)
        cards = list(generator)
        expected = [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999"
        ]
        assert cards == expected

    def test_invalid_range(self):
        """Тест с некорректным диапазоном"""
        generator = card_number_generator(10, 5)
        cards = list(generator)
        assert cards == []
