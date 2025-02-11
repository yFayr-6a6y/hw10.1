def mask_account_card(card_info):
    import re

    def mask_card_number(number):
        return number[:4] + ' ' + number[4:6] + '** **** ' + number[-4:]

    def mask_account_number(number):
        return '**' + number[-4:]

    card_pattern = re.compile(r"(Visa|Maestro) (\d{16})")
    account_pattern = re.compile(r"(Счет) (\d{20})")

    if card_pattern.match(card_info):
        card_type, card_number = card_pattern.match(card_info).groups()
        return f"{card_type} {mask_card_number(card_number)}"
    elif account_pattern.match(card_info):
        account_type, account_number = account_pattern.match(card_info).groups()
        return f"{account_type} {mask_account_number(account_number)}"
    else:
        return card_info

def get_date(date_str):
    from datetime import datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj.strftime("%d.%m.%Y")