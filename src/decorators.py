import functools
import time
import datetime
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename: Если указан, логи пишутся в файл, иначе в консоль

    Returns:
        Декоратор функции
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Логирование начала
            start_message = f"{func.__name__} - начало выполнения"
            if filename:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(f"{timestamp}: {start_message}\n")
                    if args or kwargs:
                        f.write(f"  Аргументы: args={args}, kwargs={kwargs}\n")
            else:
                print(f"{timestamp}: {start_message}")
                if args or kwargs:
                    print(f"  Аргументы: args={args}, kwargs={kwargs}")

            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time

                # Логирование успешного завершения
                success_message = f"{func.__name__} - успешно завершена"
                result_message = f"  Результат: {result}"
                time_message = f"  Время выполнения: {elapsed_time:.4f} сек"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f"{timestamp}: {success_message}\n")
                        f.write(f"{result_message}\n")
                        f.write(f"{time_message}\n")
                else:
                    print(f"{timestamp}: {success_message}")
                    print(result_message)
                    print(time_message)

                return result

            except Exception as e:
                elapsed_time = time.time() - start_time

                # Логирование ошибки
                error_message = f"{func.__name__} - ошибка"
                error_details = f"  Исключение: {type(e).__name__}: {e}"
                time_message = f"  Время выполнения: {elapsed_time:.4f} сек"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f"{timestamp}: {error_message}\n")
                        f.write(f"{error_details}\n")
                        f.write(f"{time_message}\n")
                else:
                    print(f"{timestamp}: {error_message}")
                    print(error_details)
                    print(time_message)

                raise

        return wrapper

    return decorator
