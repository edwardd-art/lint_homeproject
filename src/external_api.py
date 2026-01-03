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

    def get_exchange_rate(
            self,
            from_currency: str,
            to_currency: str = "RUB"
    ) -> Optional[float]:
        """
        Получает курс валюты к рублю.

        Args:
            from_currency: Исходная валюта (USD, EUR)
            to_currency: Целевая валюта (по умолчанию RUB)

        Returns:
            Курс обмена как float или None в случае ошибки
        """
        # Приводим валюту к верхнему регистру
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Если валюта уже рубли
        if from_currency == "RUB":
            return 1.0

        try:
            url = f"{self.base_url}/latest"
            headers = {"apikey": self.api_key}
            params = {
                "base": from_currency,
                "symbols": to_currency
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()  # Проверяем статус ответа

            data = response.json()

            # Проверяем структуру ответа
            if not data.get("success", True):
                print(f"API вернуло ошибку: {data.get('error', 'Unknown error')}")
                return None

            rates = data.get("rates", {})
            if not rates:
                print(f"Курсы валют не найдены в ответе API")
                return None

            rate = rates.get(to_currency)
            if rate is None:
                print(f"Курс {from_currency} -> {to_currency} не найден")
                return None

            # Преобразуем в float
            return float(rate)

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
        transaction: Словарь с данными транзакции

    Returns:
        Сумма в рублях как float или None в случае ошибки
    """
    try:
        # Проверяем обязательные поля
        if "amount" not in transaction:
            print("Транзакция не содержит поле 'amount'")
            return None

        if "currency" not in transaction:
            print("Транзакция не содержит поле 'currency'")
            return None

        # Получаем сумму и валюту
        amount_str = transaction["amount"]
        currency_str = transaction["currency"]

        # Преобразуем сумму в float
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            print(f"Некорректное значение суммы: {amount_str}")
            return None

        # Приводим валюту к верхнему регистру
        currency = str(currency_str).upper()

        # Если валюта уже рубли
        if currency == "RUB":
            return float(amount)

        # Проверяем поддерживаемые валюты
        supported_currencies = ["USD", "EUR", "GBP", "CNY", "JPY"]
        if currency not in supported_currencies:
            print(f"Неподдерживаемая валюта: {currency}")
            return None

        # Для других валют получаем курс через API
        try:
            api = ExchangeRateAPI()
            rate = api.get_exchange_rate(currency)

            if rate is None:
                print(f"Не удалось получить курс для {currency}")
                return None

            # Конвертируем и возвращаем как float
            result = amount * rate
            return float(result)

        except ValueError as e:
            print(f"Ошибка инициализации API: {e}")
            return None

    except Exception as e:
        print(f"Неожиданная ошибка при конвертации: {e}")
        return None