def get_mask_card_number(card_number):
    """Функция принимает на вход номер карты в виде числа и возвращает маску номера по правилу XXXX XX** **** XXXX"""
    card_number_1 = card_number[0:4]  # "1234"
    card_number_2 = card_number[4:6] + "**"  # "56" + "**" = "56**"
    card_number_3 = "****"  # всегда "****"
    card_number_4 = card_number[-4:]  # "3456"

    secret_card_number = " ".join([card_number_1, card_number_2, card_number_3, card_number_4])

    return secret_card_number


def get_mask_account(bank_account):
    """Функция принимает на вход номер счета в виде числа и возвращает маску номера по правилу **XXXX"""
    bank_account_1 = "**"  # всегда "**"
    bank_account_2 = bank_account[-4:]

    secret_bank_account = bank_account_1 + bank_account_2
    return secret_bank_account
