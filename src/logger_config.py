import logging
from pathlib import Path

# Создаем папку logs, если её нет
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)


def setup_module_logger(module_name: str) -> logging.Logger:
    """
    Настройка логгера для конкретного модуля

    Args:
        module_name: Имя модуля (mask или utils)

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Создаем логгер для модуля
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие обработчики (чтобы не дублировались записи)
    if logger.handlers:
        logger.handlers.clear()

    # Создаем обработчик для записи в файл
    log_file = log_dir / f'{module_name}.log'
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер с нужным форматом
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger
