import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения
load_dotenv()


class ExchangeRateAPI:
    """Класс для работы с API курсов валют"""

    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.base_url = os.getenv(
            "EXCHANGE_API_URL",
            "https://api.apilayer.com/exchangerates_data"
        )

        if not self.api_key:
            raise ValueError("API_KEY не найден в переменных окружения")

    def convert_currency(
            self,
            amount: float,
            from_currency: str,
            to_currency: str = "RUB"
    ) -> Optional[float]:
        """
        Конвертирует сумму из одной валюты в другую.

        Args:
            amount: Сумма для конвертации
            from_currency: Исходная валюта (USD, EUR и т.д.)
            to_currency: Целевая валюта (по умолчанию RUB)

        Returns:
            Конвертированная сумма как float или None в случае ошибки
        """
        # Приводим валюты к верхнему регистру
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Если валюта уже рубли
        if from_currency == "RUB":
            return amount

        try:
            url = f"{self.base_url}/convert"
            headers = {"apikey": self.api_key}
            params = {
                "from": from_currency,
                "to": to_currency,
                "amount": amount
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()  # Проверяем статус ответа

            data = response.json()

            # Проверяем успешность запроса
            if not data.get("success", False):
                print(f"API вернуло ошибку: {data.get('error', {}).get('info', 'Unknown error')}")
                return None

            # Получаем результат конвертации
            result = data.get("result")
            if result is None:
                print("Результат конвертации не найден в ответе API")
                return None

            return float(result)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            print(f"Ошибка обработки ответа API: {e}")
            return None


def convert_amount_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции из operations.json

    Returns:
        Сумма в рублях как float или None в случае ошибки
    """
    try:
        # Проверяем структуру транзакции
        if "operationAmount" not in transaction:
            print("Транзакция не содержит поле 'operationAmount'")
            return None

        operation_amount = transaction["operationAmount"]

        # Получаем сумму
        if "amount" not in operation_amount:
            print("Транзакция не содержит поле 'amount'")
            return None

        # Получаем валюту
        if "currency" not in operation_amount:
            print("Транзакция не содержит поле 'currency'")
            return None

        currency_info = operation_amount["currency"]

        if "code" not in currency_info:
            print("Информация о валюте не содержит поле 'code'")
            return None

        # Получаем сумму и код валюты
        amount_str = operation_amount["amount"]
        currency_code = currency_info["code"]

        # Преобразуем сумму в float
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            print(f"Некорректное значение суммы: {amount_str}")
            return None

        # Приводим код валюты к верхнему регистру
        currency = str(currency_code).upper()

        # Если валюта уже рубли
        if currency == "RUB":
            return float(amount)

        # Для других валют конвертируем через API
        try:
            api = ExchangeRateAPI()
            converted_amount = api.convert_currency(amount, currency, "RUB")

            return converted_amount

        except ValueError as e:
            print(f"Ошибка инициализации API: {e}")
            return None

    except Exception as e:
        print(f"Неожиданная ошибка при конвертации: {e}")
        return None