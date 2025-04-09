import logging
import os
from pathlib import Path

import pandas as pd

logger = logging.getLogger("data_reader")
logger.setLevel(logging.INFO)

logger.handlers = []

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

if os.path.exists(log_dir) and not os.path.isdir(log_dir):
    raise FileExistsError(f"Путь {log_dir} существует, но это не папка")
elif not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "data_reader.log")
handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - data_reader - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


def _convert_flat_to_nested(flat_transaction: dict) -> dict:
    """
    Преобразует плоский словарь из pandas в вложенный формат.

    Args:
        flat_transaction (dict): Плоский словарь, например,
            {"operationAmount.amount": 100.50, "operationAmount.currency.code": "USD"}

    Returns:
        dict: Вложенный словарь, например,
            {"operationAmount": {"amount": 100.50, "currency": {"code": "USD"}}}
    """
    nested_transaction = {}
    for key, value in flat_transaction.items():
        # Разбиваем ключ на части, "operationAmount.currency.code" -> ["operationAmount", "currency", "code"]
        parts = key.split(".")
        current = nested_transaction
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = value
            else:
                current = current.setdefault(part, {})
    return nested_transaction


def read_csv_transactions(file_path: str) -> list:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        list: Список словарей с транзакциями.
    """
    logger.info(f"Начало чтения транзакций из CSV-файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не существует")
        return []

    if Path(file_path).suffix.lower() != ".csv":
        logger.error(f"Файл {file_path} не является CSV-файлом")
        raise ValueError(f"File {file_path} is not a CSV file")

    try:
        df = pd.read_csv(file_path)

        flat_transactions = df.to_dict("records")

        transactions = [_convert_flat_to_nested(tx) for tx in flat_transactions]
        logger.info(f"Транзакции успешно загружены из CSV, количество: {len(transactions)}")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка чтения CSV-файла {file_path}: {e}")
        return []


def read_excel_transactions(file_path: str) -> list:
    """
    Считывает финансовые операции из Excel-файла (XLSX или XLS).

    Args:
        file_path (str): Путь к Excel-файлу.

    Returns:
        list: Список словарей с транзакциями.
    """
    logger.info(f"Начало чтения транзакций из Excel-файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не существует")
        return []

    if Path(file_path).suffix.lower() not in [".xlsx", ".xls"]:
        logger.error(f"Файл {file_path} не является Excel-файлом")
        raise ValueError(f"File {file_path} is not an Excel file")

    try:
        df = pd.read_excel(file_path, engine="openpyxl")

        flat_transactions = df.to_dict("records")

        transactions = [_convert_flat_to_nested(tx) for tx in flat_transactions]
        logger.info(f"Транзакции успешно загружены из Excel, количество: {len(transactions)}")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка чтения Excel-файла {file_path}: {e}")
        return []
