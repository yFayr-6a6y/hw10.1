import logging
import os
from pathlib import Path

import pandas as pd

# Настройка логирования
logger = logging.getLogger("data_reader")
logger.setLevel(logging.INFO)

logger.handlers = []

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

try:
    if os.path.exists(log_dir) and not os.path.isdir(log_dir):
        logger.error(f"Путь {log_dir} существует, но это не папка")
        raise FileExistsError(f"Path {log_dir} exists but is not a directory")
    elif not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
except Exception as e:
    logger.error(f"Не удалось создать папку для логов {log_dir}: {e}")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - data_reader - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
else:
    log_file = os.path.join(log_dir, "data_reader.log")
    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - data_reader - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def _convert_flat_to_nested(flat_transaction: dict) -> dict:
    """
    Преобразует плоский словарь из pandas в вложенный формат, адаптированный для новой структуры данных.

    Args:
        flat_transaction (dict): Плоский словарь, например,
            {"amount": 16210, "currency_code": "PEN"}

    Returns:
        dict: Вложенный словарь, например,
            {"operationAmount": {"amount": 16210, "currency": {"code": "PEN"}}}
    """
    nested_transaction = {}
    for key, value in flat_transaction.items():
        if pd.isna(value):
            continue
        nested_transaction[key] = value

    operation_amount = {}
    if "amount" in flat_transaction:
        operation_amount["amount"] = flat_transaction["amount"]
    if "currency_code" in flat_transaction:
        operation_amount["currency"] = {"code": flat_transaction["currency_code"]}
    if operation_amount:
        nested_transaction["operationAmount"] = operation_amount

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
        df = pd.read_csv(file_path, sep=";")

        required_columns = ["id", "amount", "currency_code"]
        if not all(col in df.columns for col in required_columns):
            logger.error(f"CSV файл {file_path} не содержит всех обязательных столбцов: {required_columns}")
            return []

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

        required_columns = ["id", "amount", "currency_code"]
        if not all(col in df.columns for col in required_columns):
            logger.error(f"Excel файл {file_path} не содержит всех обязательных столбцов: {required_columns}")
            return []

        flat_transactions = df.to_dict("records")

        transactions = [_convert_flat_to_nested(tx) for tx in flat_transactions]
        logger.info(f"Транзакции успешно загружены из Excel, количество: {len(transactions)}")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка чтения Excel-файла {file_path}: {e}")
        return []