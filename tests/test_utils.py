# ====== Тесты для функции search_transactions ======

def test_search_transactions_found():
    """Тест поиска существующей строки в описании"""
    from src.utils import search_transactions

    transactions = [
        {"id": 1, "description": "Перевод на карту"},
        {"id": 2, "description": "Оплата счета"},
        {"id": 3, "description": "Покупка товаров"},
        {"id": 4, "description": "Перевод другу"},
    ]

    result = search_transactions(transactions, "Перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 4


def test_search_transactions_case_insensitive():
    """Тест поиска без учета регистра"""
    from src.utils import search_transactions

    transactions = [
        {"id": 1, "description": "перевод на карту"},
        {"id": 2, "description": "ОПЛАТА СЧЕТА"},
        {"id": 3, "description": "Покупка товаров"},
    ]

    result = search_transactions(transactions, "ПЕРЕВОД")
    assert len(result) == 1
    assert result[0]["id"] == 1

    result = search_transactions(transactions, "оплата")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_transactions_not_found():
    """Тест поиска отсутствующей строки"""
    from src.utils import search_transactions

    transactions = [
        {"id": 1, "description": "Перевод на карту"},
        {"id": 2, "description": "Оплата счета"},
    ]

    result = search_transactions(transactions, "Покупка")
    assert len(result) == 0


def test_search_transactions_empty_string():
    """Тест поиска с пустой строкой"""
    from src.utils import search_transactions

    transactions = [
        {"id": 1, "description": "Перевод на карту"},
        {"id": 2, "description": "Оплата счета"},
    ]

    result = search_transactions(transactions, "")
    assert len(result) == 2


def test_search_transactions_empty_list():
    """Тест поиска в пустом списке"""
    from src.utils import search_transactions

    result = search_transactions([], "Перевод")
    assert result == []


def test_search_transactions_no_description():
    """Тест поиска когда у транзакции нет поля description"""
    from src.utils import search_transactions

    transactions = [
        {"id": 1, "amount": 1000},
        {"id": 2, "description": "Перевод на карту"},
    ]

    result = search_transactions(transactions, "Перевод")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_transactions_regex_special_chars():
    """Тест поиска со спецсимволами (должны экранироваться)"""
    from src.utils import search_transactions

    transactions = [
        {"id": 1, "description": "Перевод (на карту)"},
        {"id": 2, "description": "Перевод на карту"},
    ]

    result = search_transactions(transactions, "(на")
    assert len(result) == 1
    assert result[0]["id"] == 1


# ====== Тесты для функции count_transactions_by_category ======

def test_count_transactions_by_category_success():
    """Тест успешного подсчета транзакций по категориям"""
    from src.utils import count_transactions_by_category

    transactions = [
        {"id": 1, "description": "Перевод на карту"},           # Перевод
        {"id": 2, "description": "Оплата счета"},               # Оплата
        {"id": 3, "description": "Покупка товаров"},            # Покупка
        {"id": 4, "description": "Перевод другу"},              # Перевод
        {"id": 5, "description": "Оплата коммунальных услуг"},  # Оплата
    ]

    categories = ["Перевод", "Оплата", "Покупка"]

    result = count_transactions_by_category(transactions, categories)

    assert result["Перевод"] == 2   # id 1 и 4
    assert result["Оплата"] == 2    # id 2 и 5
    assert result["Покупка"] == 1   # id 3


def test_count_transactions_by_category_case_insensitive():
    """Тест подсчета категорий без учета регистра"""
    from src.utils import count_transactions_by_category

    transactions = [
        {"id": 1, "description": "перевод на карту"},
        {"id": 2, "description": "ОПЛАТА счета"},
        {"id": 3, "description": "Покупка товаров"},
    ]

    categories = ["Перевод", "Оплата", "Покупка"]

    result = count_transactions_by_category(transactions, categories)

    assert result["Перевод"] == 1
    assert result["Оплата"] == 1
    assert result["Покупка"] == 1


def test_count_transactions_by_category_with_zero():
    """Тест категорий с нулевым количеством"""
    from src.utils import count_transactions_by_category

    transactions = [
        {"id": 1, "description": "Перевод на карту"},
        {"id": 2, "description": "Перевод другу"},
    ]

    categories = ["Перевод", "Оплата", "Покупка"]

    result = count_transactions_by_category(transactions, categories)

    assert result["Перевод"] == 2
    assert result["Оплата"] == 0
    assert result["Покупка"] == 0


def test_count_transactions_by_category_empty_list():
    """Тест подсчета с пустым списком транзакций"""
    from src.utils import count_transactions_by_category

    categories = ["Перевод", "Оплата"]

    result = count_transactions_by_category([], categories)

    assert result["Перевод"] == 0
    assert result["Оплата"] == 0


def test_count_transactions_by_category_empty_categories():
    """Тест подсчета с пустым списком категорий"""
    from src.utils import count_transactions_by_category

    transactions = [
        {"id": 1, "description": "Перевод на карту"},
    ]

    result = count_transactions_by_category(transactions, [])

    assert result == {}


def test_count_transactions_by_category_no_description():
    """Тест транзакций без поля description"""
    from src.utils import count_transactions_by_category

    transactions = [
        {"id": 1, "amount": 1000},
        {"id": 2, "description": "Перевод на карту"},
        {"id": 3, "amount": 500},
    ]

    categories = ["Перевод", "Оплата"]

    result = count_transactions_by_category(transactions, categories)

    assert result["Перевод"] == 1  # только id 2
    assert result["Оплата"] == 0


def test_count_transactions_by_category_partial_match():
    """Тест частичного совпадения (категория внутри описания)"""
    from src.utils import count_transactions_by_category

    transactions = [
        {"id": 1, "description": "Перевод на карту"},
        {"id": 2, "description": "Банковский перевод"},
        {"id": 3, "description": "Переводы между счетами"},
    ]

    categories = ["Перевод"]

    result = count_transactions_by_category(transactions, categories)

    # Все три транзакции содержат слово "Перевод"
    assert result["Перевод"] == 3