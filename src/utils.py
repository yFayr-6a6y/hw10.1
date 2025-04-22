import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List

from .data_reader import read_csv_transactions, read_excel_transactions
from .external_api import convert_to_rub

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

logger.handlers = []

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")

if os.path.exists(log_dir) and not os.path.isdir(log_dir):
    raise FileExistsError(f"Путь {log_dir} существует, но это не папка")
elif not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "utils.log")
handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - utils - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


def load_transactions(file_path: str) -> list:
    """
    Загружает транзакции из файла (JSON, CSV или XLSX).

    Args:
        file_path (str): Путь к файлу с транзакциями.

    Returns:
        list: Список транзакций в формате списка словарей.
    """
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл {file_path} не существует")
        return []

    file_extension = Path(file_path).suffix.lower()

    try:
        if file_extension == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                transactions = json.load(f)
            logger.info(f"Транзакции успешно загружены из JSON, количество: {len(transactions)}")
            return transactions

        elif file_extension == ".csv":
            transactions = read_csv_transactions(file_path)
            return transactions

        elif file_extension in [".xlsx", ".xls"]:
            transactions = read_excel_transactions(file_path)
            return transactions

        else:
            logger.error(f"Неподдерживаемый формат файла: {file_extension}")
            raise ValueError(f"Unsupported file format: {file_extension}")

    except Exception as e:
        logger.error(f"Ошибка загрузки файла {file_path}: {e}")
        return []


def get_transaction_amount_rub(transaction):
    """Возвращает сумму транзакции в рублях."""
    logger.info("Начало конвертации суммы транзакции в рубли")
    if not isinstance(transaction, dict):
        logger.error(f"Transaction должен быть словарем, получено: {type(transaction)}")
        raise TypeError("Transaction must be a dictionary.")

    if "operationAmount" not in transaction:
        logger.error("В транзакции отсутствует ключ 'operationAmount'")
        raise ValueError("Transaction must have 'operationAmount' key.")

    operation_amount = transaction["operationAmount"]
    amount = operation_amount.get("amount")
    if amount is None:
        logger.error("В 'operationAmount' отсутствует ключ 'amount'")
        raise ValueError("Transaction must have 'amount' in 'operationAmount'")
    amount = float(amount)
    currency_dict = operation_amount.get("currency", {"code": "RUB"})
    currency_code = currency_dict.get("code", "RUB")

    logger.debug(f"Сумма: {amount}, валюта: {currency_code}")

    if currency_code != "RUB":
        logger.info(f"Конвертация {amount} {currency_code} в RUB")
        converted_amount = convert_to_rub(amount, currency_code)
        if converted_amount is None:
            logger.error(f"Не удалось конвертировать {amount} {currency_code} в RUB")
            raise ValueError(f"Could not convert {currency_code} to RUB")
        logger.info(f"Сумма после конвертации: {converted_amount} RUB")
        return converted_amount
    else:
        logger.info(f"Транзакция уже в RUB: {amount}")
        return amount


def filter_transactions_by_description(transactions: List[Dict], search_string: str) -> List[Dict]:
    """
    Фильтрует список транзакций по строке поиска в описании с использованием регулярных выражений.

    Args:
        transactions (List[Dict]): Список словарей с данными о транзакциях.
        search_string (str): Строка для поиска в описании.

    Returns:
        List[Dict]: Отфильтрованный список транзакций, где в описании есть совпадение.
    """
    logger.info(f"Фильтрация транзакций по описанию с поисковой строкой: {search_string}")
    if not search_string:
        logger.info("Поисковая строка пуста, возвращаем исходный список транзакций")
        return transactions

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    filtered_transactions = []
    for transaction in transactions:
        if "description" not in transaction:
            logger.debug(f"Транзакция {transaction.get('id', 'без ID')} пропущена: отсутствует поле 'description'")
            continue
        if pattern.search(transaction["description"]):
            filtered_transactions.append(transaction)
            logger.debug(f"Транзакция {transaction.get('id', 'без ID')} соответствует поисковой строке")

    logger.info(f"Найдено {len(filtered_transactions)} транзакций, соответствующих поисковой строке")
    return filtered_transactions


def count_transactions_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по заданным категориям.

    Args:
        transactions (List[Dict]): Список словарей с данными о транзакциях.
        categories (List[str]): Список категорий для подсчёта.

    Returns:
        Dict[str, int]: Словарь, где ключи — категории, а значения — количество операций.
    """
    logger.info("Подсчёт транзакций по категориям")
    category_counts = {category: 0 for category in categories}

    for transaction in transactions:
        if "description" not in transaction:
            logger.debug(f"Транзакция {transaction.get('id', 'без ID')} пропущена: отсутствует поле 'description'")
            continue
        description = transaction["description"]
        for category in categories:
            if category.lower() in description.lower():
                category_counts[category] += 1
                logger.debug(f"Транзакция {transaction.get('id', 'без ID')} отнесена к категории {category}")
                break

    logger.info(f"Результат подсчёта по категориям: {category_counts}")
    return category_counts