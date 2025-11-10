from src.widget import mask_account_card, get_date
import pytest

# Фикстуры
@pytest.fixture
def account_card():
    return "Счет 73654108430135874305"

@pytest.fixture
def visa_card():
    return "Visa Platinum 7000792289606361"

# Тесты для mask_account_card
@pytest.mark.parametrize("account_input, expected", [
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 12345678901234567890", "Счет **7890"),
])
def test_mask_account_card_account(account_input, expected):
    assert mask_account_card(account_input) == expected

@pytest.mark.parametrize("card_input, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Mastercard 1234567890123456", "Mastercard 1234 56** **** 3456"),
])
def test_mask_account_card_cards(card_input, expected):
    assert mask_account_card(card_input) == expected

# Тесты для get_date
@pytest.mark.parametrize("date_input, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
])
def test_get_date(date_input, expected):
    assert get_date(date_input) == expected