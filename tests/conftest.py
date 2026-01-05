import pytest
import os


@pytest.fixture(autouse=True)
def setup_env_vars():
    """Фикстура для установки переменных окружения для тестов"""
    # Сохраняем оригинальные значения
    original_api_key = os.environ.get("API_KEY")
    original_api_url = os.environ.get("EXCHANGE_API_URL")

    # Устанавливаем тестовые значения
    os.environ["API_KEY"] = "test_api_key_1234567890"
    os.environ["EXCHANGE_API_URL"] = "https://api.test.com"

    yield

    # Восстанавливаем оригинальные значения
    if original_api_key is not None:
        os.environ["API_KEY"] = original_api_key
    else:
        os.environ.pop("API_KEY", None)

    if original_api_url is not None:
        os.environ["EXCHANGE_API_URL"] = original_api_url
    else:
        os.environ.pop("EXCHANGE_API_URL", None)
