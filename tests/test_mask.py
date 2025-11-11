import pytest

from src.mask import get_mask_account, get_mask_card_number


# Фикстуры
@pytest.fixture
def visa_card():
    return "4234567890123456"


@pytest.fixture
def sample_account():
    return "73654108430135874305"


# Тесты для карт
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_mask_cards(visa_card, card_number, expected):
    assert get_mask_card_number(card_number) == expected
    visa_result = get_mask_card_number(visa_card)
    assert visa_result.startswith("4234")


# Тесты для счетов
@pytest.mark.parametrize(
    "account, expected",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
    ],
)
def test_mask_accounts(sample_account, account, expected):
    assert get_mask_account(account) == expected
    assert get_mask_account(sample_account) == "**4305"
