import pytest
def filter_by_currency(transactions, currency_code):
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


transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 3, "operationAmount": {"currency": {"code": "EUR"}}},
    {"id": 4}  # Без operationAmount
]


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 2),
        ("EUR", 1),
        ("GBP", 0),
    ],
)
def test_filter_by_currency(currency, expected_count):
    """Проверяет фильтрацию транзакций по валюте."""
    filtered = list(filter_by_currency(transactions, currency))
    assert len(filtered) == expected_count
    for transaction in filtered:
        assert transaction["operationAmount"]["currency"]["code"] == currency


def test_filter_by_currency_empty_list():
    """Проверяет обработку пустого списка."""
    filtered = list(filter_by_currency([], "USD"))
    assert len(filtered) == 0


def test_filter_by_currency_no_operation_amount():
    """Проверяет, что транзакции без operationAmount игнорируются."""
    filtered = list(filter_by_currency([{"id": 1}], "USD"))
    assert len(filtered) == 0





def transaction_descriptions(transactions):
    if not transactions:
        yield "Транзакции отсутствуют"
        return

    for transaction in transactions:
        description = transaction.get('description')  # Используем .get(), чтобы избежать KeyError

        if description is None:
            yield "Описание отсутствует"
        else:
            yield description

@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        (
            [
                {'amount': 100, 'description': 'Зарплата', 'type': 'deposit'},
                {'amount': 50, 'description': 'Покупка', 'type': 'withdrawal'},
                {'amount': 25, 'description': 'Другу', 'type': 'transfer'},
            ],
            [
                "Зачисление: Зарплата, сумма: 100",
                "Снятие: Покупка, сумма: 50",
                "Перевод: Другу, сумма: 25",
            ],
        ),
        (
            [
                {'amount': 100, 'description': 'Зарплата', 'type': 'deposit'},
                {'amount': 50, 'description': 'Покупка', 'type': 'withdrawal'},
                {'amount': 25, 'description': 'Другу', 'type': 'transfer'},
                {'amount': 10, 'description': 'Бонус', 'type': 'unknown'}
            ],
            [
                "Зачисление: Зарплата, сумма: 100",
                "Снятие: Покупка, сумма: 50",
                "Перевод: Другу, сумма: 25",
                "Неизвестный тип транзакции: unknown"
            ],
        ),
        (
            [
                {'amount': 100, 'description': 'Зарплата'},
                {'amount': 50, 'type': 'withdrawal'},
                {'description': 'Другу', 'type': 'transfer'},
            ],
            [
                "Некорректные данные транзакции",
                "Некорректные данные транзакции",
                "Некорректные данные транзакции",
            ],
        ),
        ([], []),
    ],
)
def test_transaction_descriptions(transactions, expected_descriptions):
    assert list(transaction_descriptions(transactions)) == expected_descriptions





def card_number_generator(start, end):
    for number in range(start, end + 1):
        card_number_str = str(number).zfill(16)

        formatted_card_number = (
            f"{card_number_str[0:4]} {card_number_str[4:8]} "
            f"{card_number_str[8:12]} {card_number_str[12:16]}"
        )
        yield formatted_card_number
@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999998, 10000000000000000, ["9999 9999 9999 9998", "9999 9999 9999 9999", "0000 0000 0000 0000"]),
        (5, 4, []),
    ],
)
def test_card_number_generator_range(start, end, expected_numbers):
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected_numbers

def test_card_number_generator_formatting():
    generated_number = next(card_number_generator(10, 10))
    assert len(generated_number) == 19
    assert generated_number.count(" ") == 3
    assert all(c.isdigit() or c == " " for c in generated_number)