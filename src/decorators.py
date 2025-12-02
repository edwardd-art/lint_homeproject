import functools
from datetime import datetime
from typing import Callable, Any


def log(filename: str | None = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: если указан - логи в файл, иначе - в консоль

    Returns:
        Декоратор для функции
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Логируем начало выполнения
            start_time = datetime.now()
            func_name = func.__name__

            log_message = f"{start_time} - {func_name} - начало выполнения\n"
            log_message += f"Аргументы: args={args}, kwargs={kwargs}\n"

            try:
                # Выполняем декорируемую функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                end_time = datetime.now()
                execution_time = end_time - start_time

                log_message += f"{end_time} - {func_name} - успешно завершена\n"
                log_message += f"Результат: {result}\n"
                log_message += f"Время выполнения: {execution_time}\n"

                # Записываем логи
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Логируем ошибку
                end_time = datetime.now()
                execution_time = end_time - start_time

                log_message += f"{end_time} - {func_name} - ошибка\n"
                log_message += f"Тип ошибки: {type(e).__name__}\n"
                log_message += f"Сообщение: {str(e)}\n"
                log_message += f"Время выполнения до ошибки: {execution_time}\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                raise

        return wrapper

    return decorator