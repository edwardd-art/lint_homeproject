from src.mask import get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция принимает один аргумент — строку,
    содержащую тип и номер карты или счета
    и возвращает строку с замаскированным номером"""

    if "Счет" in account_card:
        # код для счета
        number_account = account_card.split()
        number = number_account[-1]
        number_1 = "**"  # всегда "**"
        number_2 = number[-4:]
        secret_account_card = number_1 + number_2
        return f"Счет {secret_account_card}"  # Добавляем "Счет" обратно

    else:
        # код для карты
        parts = account_card.split()
        card_number = parts[-1]
        masked_card = get_mask_card_number(card_number)  # Эта функция должна быть доступна
        card_type = " ".join(parts[:-1])  # "Visa Platinum"
        result = f"{card_type} {masked_card}"

        return result  # Возвращаем результат, а не вызываем функцию

def get_date(date: str) -> str:
    """Функция которая, принимает на вход строку
    с датой и возвращает строку с датой в формате ("ДД.ММ.ГГГГ" "11.03.2024")"""
    # "2024-03-11T02:26:18.671407"
    days = date[8:10]
    month = date[5:7]
    year = date[0:4]
    new_date = ".".join([days, month, year])

    return new_date