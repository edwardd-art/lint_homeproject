import pytest
import tempfile
import os
from src.decorators import log


# Тестовая функция для декорирования
def add(a: int, b: int) -> int:
    """Простая функция сложения для тестирования."""
    return a + b


def divide(a: int, b: int) -> float:
    """Функция деления, которая может вызвать ошибку."""
    return a / b


# Тесты для логирования в консоль
def test_log_to_console_success(capsys):
    """Тест успешного выполнения с выводом в консоль."""
    decorated_add = log()(add)

    result = decorated_add(2, 3)

    # Проверяем результат
    assert result == 5

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add - начало выполнения" in captured.out
    assert "add - успешно завершена" in captured.out
    assert "Результат: 5" in captured.out


def test_log_to_console_error(capsys):
    """Тест ошибки с выводом в консоль."""
    decorated_divide = log()(divide)

    # Проверяем что ошибка пробрасывается
    with pytest.raises(ZeroDivisionError):
        decorated_divide(5, 0)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "divide - начало выполнения" in captured.out
    assert "divide - ошибка" in captured.out
    assert "ZeroDivisionError" in captured.out


# Тесты для логирования в файл
def test_log_to_file_success():
    """Тест успешного выполнения с записью в файл."""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as tmp:
        tmp_file = tmp.name

    try:
        decorated_add = log(filename=tmp_file)(add)

        result = decorated_add(10, 20)

        # Проверяем результат
        assert result == 30

        # Проверяем запись в файл
        with open(tmp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "add - начало выполнения" in content
            assert "add - успешно завершена" in content
            assert "Результат: 30" in content

    finally:
        # Удаляем временный файл
        os.unlink(tmp_file)


def test_log_to_file_error():
    """Тест ошибки с записью в файл."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as tmp:
        tmp_file = tmp.name

    try:
        decorated_divide = log(filename=tmp_file)(divide)

        # Проверяем что ошибка пробрасывается
        with pytest.raises(ZeroDivisionError):
            decorated_divide(10, 0)

        # Проверяем запись в файл
        with open(tmp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "divide - начало выполнения" in content
            assert "divide - ошибка" in content
            assert "ZeroDivisionError" in content

    finally:
        os.unlink(tmp_file)


# Тест с различными аргументами
def test_log_with_args_kwargs(capsys):
    """Тест с позиционными и именованными аргументами."""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")

    assert result == "Hi, Alice!"

    captured = capsys.readouterr()
    assert "greet - начало выполнения" in captured.out
    assert "Аргументы: args=('Alice',), kwargs={'greeting': 'Hi'}" in captured.out
    assert "Результат: Hi, Alice!" in captured.out


# Тест сохранения метаданных функции
def test_log_preserves_metadata():
    """Тест что декоратор сохраняет метаданные функции."""

    @log()
    def example():
        """Тестовая функция."""
        return 42

    assert example.__name__ == "example"
    assert example.__doc__ == "Тестовая функция."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
