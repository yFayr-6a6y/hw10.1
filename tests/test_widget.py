import pytest
import re

def mask_account_card(s: str) -> str:
    """Маскирует карту/счет или возвращает исходную строку."""
    m = re.match(r"(Visa|Maestro) (\d{16})", s)
    if m: return f"{m[1]} {m[2][:4]} {m[2][4:6]}** **** {m[2][-4:]}"
    m = re.match(r"(Счет) (\d{20})", s)
    if m: return f"{m[1]} **{m[2][-4:]}"
    return s

@pytest.mark.parametrize(
    "s, expected",
    [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("Maestro 9876543210987654", "Maestro 9876 54** **** 7654"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Неизвестный формат", "Неизвестный формат"),
        ("", ""),
    ],
)
def test_mask_account_card(s, expected):
    assert mask_account_card(s) == expected