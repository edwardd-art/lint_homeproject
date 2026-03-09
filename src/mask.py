from src.logger_config import setup_module_logger

# Создаем логгер для модуля mask
logger = setup_module_logger('mask')


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты в виде числа и возвращает маску номера по правилу XXXX XX** **** XXXX"""
    try:
        logger.info(f"Начало маскирования карты. Номер: {card_number[:4]}...{card_number[-4:]}")

        card_number_1 = card_number[0:4]  # "1234"
        card_number_2 = card_number[4:6] + "**"  # "56" + "**" = "56**"
        card_number_3 = "****"  # всегда "****"
        card_number_4 = card_number[-4:]  # "3456"

        secret_card_number = " ".join([card_number_1, card_number_2, card_number_3, card_number_4])

        logger.info(f"Карта успешно замаскирована: {secret_card_number}")
        return secret_card_number

    except Exception as e:
        logger.error(f"Ошибка при маскировании карты: {e}")
        raise


def get_mask_account(bank_account: str) -> str:
    """Функция принимает на вход номер счета в виде числа и возвращает маску номера по правилу **XXXX"""
    try:
        logger.info(f"Начало маскирования счета. Номер: ...{bank_account[-4:]}")

        bank_account_1 = "**"  # всегда "**"
        bank_account_2 = bank_account[-4:]

        secret_bank_account = bank_account_1 + bank_account_2

        logger.info(f"Счет успешно замаскирован: {secret_bank_account}")
        return secret_bank_account

    except Exception as e:
        logger.error(f"Ошибка при маскировании счета: {e}")
        raise
