def get_mask_card_number(card_number: int) -> str:
    """маскировка номера карты"""
    card_str = str(card_number)
    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    return masked_card


def get_mask_account(account_number: int) -> str:
    """маскировка номера счета"""
    account_str = str(account_number)
    masked_account = f"**{account_str[-4:]}"
    return masked_account


card_number = int(input("enter card number:"))
account_number = int(input("enter account number:"))

print(get_mask_card_number(card_number))
print(get_mask_account(account_number))
