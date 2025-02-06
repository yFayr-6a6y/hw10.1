from tests.test import get_mask_card_number


def mask_account_card(card: str) -> str:
    new_list = card.split(" ")
    card_num = []
    card_alph = []

    for i in new_list:
        if i.isalpha():
            card_alph.append(i)
        else:
            card_num.append(int(i))

    a = card_alph
    b = get_mask_card_number(card_num)

    return f"{a}{b}"

print(mask_account_card())ff