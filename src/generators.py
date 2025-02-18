def filter_by_currency(transactions, currency_code):
    """
    Возвращает итератор, который поочередно выдает транзакции из списка transactions,
    где валюта операции соответствует заданной (currency_code)."""
    if not transactions:
        return

    for transaction in transactions:
        operation_amount = transaction.get('operationAmount')
        if operation_amount:
            currency = operation_amount.get('currency')
            if currency:
                code = currency.get('code')
                if code == currency_code:
                    yield transaction



def transaction_descriptions(transactions):
    """Генератор, принимающий список словарей с транзакциями и возвращающий
    описание каждой операции по очереди."""
    if not transactions:
        yield "Транзакции отсутствуют"
        return

    for transaction in transactions:
        description = transaction.get('description')  # Используем .get(), чтобы избежать KeyError

        if description is None:
            yield "Описание отсутствует"
        else:
            yield description

def card_number_generator(start, end):
    """
    Генератор, выдающий номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 символов
        card_number_str = str(number).zfill(16)

        formatted_card_number = (
            f"{card_number_str[0:4]} {card_number_str[4:8]} "
            f"{card_number_str[8:12]} {card_number_str[12:16]}"
        )
        yield formatted_card_number

