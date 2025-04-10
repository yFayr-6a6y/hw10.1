import os
import pytest
import re
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_reader import read_csv_transactions, read_excel_transactions


DATA_DIR = "data"


def test_read_csv_transactions():
    """Тест чтения транзакций из CSV-файла."""
    file_path = os.path.join(DATA_DIR, "transactions.csv")
    transactions = read_csv_transactions(file_path)

    assert isinstance(transactions, list)
    assert len(transactions) == 1000
    assert transactions[0]["id"] == 650703
    assert transactions[0]["state"] == "EXECUTED"
    assert transactions[0]["operationAmount"]["amount"] == 16210
    assert transactions[0]["operationAmount"]["currency"]["code"] == "PEN"
    assert transactions[0]["from"] == "Счет 58803664561298323391"
    assert transactions[0]["to"] == "Счет 39745660563456619397"
    assert transactions[0]["description"] == "Перевод организации"


def test_read_csv_transactions_nonexistent_file():
    """Тест чтения транзакций из несуществующего CSV-файла."""
    file_path = os.path.join(DATA_DIR, "nonexistent.csv")
    transactions = read_csv_transactions(file_path)

    assert transactions == []


def test_read_csv_transactions_invalid_format():
    """Тест чтения транзакций из файла с неподдерживаемым форматом (не CSV)."""
    file_path = os.path.join(DATA_DIR, "transactions.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write('[{"id": 1}]')

    try:
        escaped_file_path = re.escape(file_path)
        with pytest.raises(ValueError, match=f"File {escaped_file_path} is not a CSV file"):
            read_csv_transactions(file_path)
    finally:
        os.remove(file_path)


def test_read_csv_transactions_missing_columns():
    """Тест чтения транзакций из CSV с отсутствующими столбцами."""
    file_path = os.path.join(DATA_DIR, "transactions_missing_columns.csv")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("wrong_column\n1\n2")

    try:
        transactions = read_csv_transactions(file_path)
        assert transactions == [], "Ожидается пустой список при отсутствии обязательных столбцов"
    finally:
        os.remove(file_path)


def test_read_excel_transactions():
    """Тест чтения транзакций из Excel-файла."""
    file_path = os.path.join(DATA_DIR, "transactions_excel.xlsx")
    transactions = read_excel_transactions(file_path)

    assert isinstance(transactions, list)
    assert len(transactions) == 1000
    assert transactions[0]["id"] == 650703
    assert transactions[0]["state"] == "EXECUTED"
    assert transactions[0]["operationAmount"]["amount"] == 16210
    assert transactions[0]["operationAmount"]["currency"]["code"] == "PEN"
    assert transactions[0]["from"] == "Счет 58803664561298323391"
    assert transactions[0]["to"] == "Счет 39745660563456619397"
    assert transactions[0]["description"] == "Перевод организации"


def test_read_excel_transactions_nonexistent_file():
    """Тест чтения транзакций из несуществующего Excel-файла."""
    file_path = os.path.join(DATA_DIR, "nonexistent.xlsx")
    transactions = read_excel_transactions(file_path)

    assert transactions == []


def test_read_excel_transactions_invalid_format():
    """Тест чтения транзакций из файла с неподдерживаемым форматом (не Excel)."""
    file_path = os.path.join(DATA_DIR, "transactions.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write('[{"id": 1}]')

    try:
        escaped_file_path = re.escape(file_path)
        with pytest.raises(ValueError, match=f"File {escaped_file_path} is not an Excel file"):
            read_excel_transactions(file_path)
    finally:
        os.remove(file_path)


def test_read_excel_transactions_missing_columns():
    """Тест чтения транзакций из Excel с отсутствующими столбцами."""
    file_path = os.path.join(DATA_DIR, "transactions_missing_columns.xlsx")
    df = pd.DataFrame({"wrong_column": [1, 2]})
    df.to_excel(file_path, index=False)

    try:
        transactions = read_excel_transactions(file_path)
        assert transactions == [], "Ожидается пустой список при отсутствии обязательных столбцов"
    finally:
        os.remove(file_path)