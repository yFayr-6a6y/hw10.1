

from src.masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(card: str | int) -> str | int:
    new_list = card.split(" ")
    card_num = []
    card_alph = []

    for i in new_list:
        if i.isalpha():
            card_alph.append(i)
        else:
            card_num.append(int(i))

    name_letter_card = ' '.join(card_alph)


    if name_letter_card == 'Счет':
        name_number_card = get_mask_account(''. join(card_num))
    else:
        name_number_card = get_mask_card_number (''.join(card_num))


    return f'{name_letter_card} {name_number_card}'

def get_date(my_date: str) -> str:
    date_object = datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S.%f")
    return date_object. strftime("2024-03-11T02:26:18.67140")



print(get_date("2024-03-11T02:26:18.67140"))
