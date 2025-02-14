import pytest

def get_mask_card_number(card_number: int) -> str:
    """Маскирует номер карты (предполагается 16 цифр)."""
    if not isinstance(card_number, int):
        raise TypeError("номер карты должен быть целым числом")
    card_str = str(card_number)
    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
        (0000000000000000, "0000 00** **** 0000"),
        (9999888877776666, "9999 88** **** 6666"),
    ],
)
def test_mask_card_number_valid(card_number, expected):
    """Тестирует маскировку валидных номеров карт."""
    assert get_mask_card_number(card_number) == expected

def test_mask_card_number_invalid_type():
    """Тестирует TypeError для некорректных типов."""
    with pytest.raises(TypeError):
        get_mask_card_number("1234567890123456")