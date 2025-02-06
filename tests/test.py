def get_mask_card_number(card_number: str) -> str | None:
    """Функция, которая принимает на вход номер карты в виде числа и возвращает
    XXXX XX** **** XXXX"""
    if len(card_number) < 16:
        print("Введите номер карты:")
    return f"{card_number[:7]} ** **** {card_number[-4:]}"


def get_mask_account(mask_account: str) -> str | None:
    """Функция, которая на вход номер счета в виде числа и возвращает маску
    номер **XXXX"""
    if len(mask_account) < 20:
        print("Введите номер счета:")
    return f"**{mask_account[-4:]}"


print(get_mask_card_number("7000792289606361"))
print(get_mask_account("70008881792289606361"))
