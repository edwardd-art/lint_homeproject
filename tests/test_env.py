# test_env.py
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем переменные
api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")

# Безопасно показываем API_KEY (первые 10 символов)
if api_key:
    print("API_KEY:", api_key[:10] + "..." if len(api_key) > 10 else api_key)
else:
    print("API_KEY: не найден!")

print("API_URL:", api_url if api_url else "не найден!")

# Дополнительная проверка
print("\nПроверка завершена успешно!" if api_key and api_url else "\nЕсть проблемы с загрузкой переменных!")