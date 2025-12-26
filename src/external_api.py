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
            Курс обмена или None в случае ошибки
        """
        if from_currency.upper() == "RUB":
            return 1.0

        try:
            url = f"{self.base_url}/latest"
            headers = {"apikey": self.api_key}
            params = {
                "base": from_currency,
                "symbols": to_currency
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            rate = data.get("rates", {}).get(to_currency)

            if rate is None:
                return None

            return float(rate)

        except requests.exceptions.RequestException:
            return None
        except (KeyError, ValueError):
            return None


def convert_amount_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Сумма в рублях или None в случае ошибки
    """
    try:
        # Проверяем обязательные поля
        if "amount" not in transaction or "currency" not in transaction:
            return None

        amount = float(transaction["amount"])
        currency = transaction["currency"].upper()

        # Если валюта уже рубли
        if currency == "RUB":
            return amount

        # Для других валют получаем курс
        api = ExchangeRateAPI()
        rate = api.get_exchange_rate(currency)

        if rate is None:
            return None

        # Конвертируем
        return amount * rate

    except (ValueError, TypeError):
        return None