import os

import pytest

from src.data_reader import read_csv_transactions, read_excel_transactions


def test_read_csv_transactions():
    """Тест чтения транзакций из CSV-файла."""
    file_path = "tests/fixtures/transactions.csv"
    transactions = read_csv_transactions(file_path)

    assert isinstance(transactions, list)
    assert len(transactions) == 2
    assert transactions[0]["id"] == 1
    assert transactions[0]["operationAmount"]["amount"] == 100.50
    assert transactions[0]["operationAmount"]["currency"]["code"] == "USD"
    assert transactions[1]["id"] == 2
    assert transactions[1]["operationAmount"]["amount"] == 200.75
    assert transactions[1]["operationAmount"]["currency"]["code"] == "RUB"


def test_read_csv_transactions_nonexistent_file():
    """Тест чтения транзакций из несуществующего CSV-файла."""
    file_path = "tests/fixtures/nonexistent.csv"
    transactions = read_csv_transactions(file_path)

    assert transactions == []


def test_read_csv_transactions_invalid_format():
    """Тест чтения транзакций из файла с неподдерживаемым форматом (не CSV)."""
    file_path = "tests/fixtures/transactions.json"
    with pytest.raises(ValueError, match="File tests/fixtures/transactions.json is not a CSV file"):
        read_csv_transactions(file_path)


def test_read_csv_transactions_missing_columns():
    """Тест чтения транзакций из CSV с отсутствующими столбцами."""
    file_path = "tests/fixtures/transactions_missing_columns.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("wrong_column\n1\n2")

    try:
        transactions = read_csv_transactions(file_path)
        assert transactions == [], "Ожидается пустой список при отсутствии обязательных столбцов"
    finally:
        os.remove(file_path)


def test_read_excel_transactions():
    """Тест чтения транзакций из Excel-файла."""
    file_path = "tests/fixtures/transactions.xlsx"
    transactions = read_excel_transactions(file_path)

    assert isinstance(transactions, list)
    assert len(transactions) == 2
    assert transactions[0]["id"] == 1
    assert transactions[0]["operationAmount"]["amount"] == 100.50
    assert transactions[0]["operationAmount"]["currency"]["code"] == "USD"
    assert transactions[1]["id"] == 2
    assert transactions[1]["operationAmount"]["amount"] == 200.75
    assert transactions[1]["operationAmount"]["currency"]["code"] == "RUB"


def test_read_excel_transactions_nonexistent_file():
    """Тест чтения транзакций из несуществующего Excel-файла."""
    file_path = "tests/fixtures/nonexistent.xlsx"
    transactions = read_excel_transactions(file_path)

    assert transactions == []


def test_read_excel_transactions_invalid_format():
    """Тест чтения транзакций из файла с неподдерживаемым форматом (не Excel)."""
    file_path = "tests/fixtures/transactions.json"
    with pytest.raises(ValueError, match="File tests/fixtures/transactions.json is not an Excel file"):
        read_excel_transactions(file_path)


def test_read_excel_transactions_missing_columns():
    """Тест чтения транзакций из Excel с отсутствующими столбцами."""
    file_path = "tests/fixtures/transactions_missing_columns.xlsx"
    import pandas as pd

    df = pd.DataFrame({"wrong_column": [1, 2]})
    df.to_excel(file_path, index=False)

    try:
        transactions = read_excel_transactions(file_path)
        assert transactions == [], "Ожидается пустой список при отсутствии обязательных столбцов"
    finally:
        os.remove(file_path)
