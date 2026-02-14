import logging
from pathlib import Path

# Создаем папку logs, если её нет
log_dir = Path(__file__).parent / 'logs'
print(f"Попытка создать папку: {log_dir}")  # Добавь эту строку для отладки

try:
    log_dir.mkdir(exist_ok=True)
    print(f"Папка создана или уже существует: {log_dir}")  # Добавь эту строку
except Exception as e:
    print(f"Ошибка при создании папки: {e}")  # Добавь эту строку


def setup_module_logger(module_name: str) -> logging.Logger:
    """Настройка логгера для конкретного модуля"""
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие обработчики
    if logger.handlers:
        logger.handlers.clear()

    # Создаем обработчик для записи в файл
    log_file = log_dir / f'{module_name}.log'
    print(f"Путь к файлу лога: {log_file}")  # Добавь эту строку

    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
