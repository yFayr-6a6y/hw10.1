import json
import logging
import os
from .external_api import convert_to_rub

logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)

logger.handlers = []

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')

if os.path.exists(log_dir) and not os.path.isdir(log_dir):
    raise FileExistsError(f"Путь {log_dir} существует, но это не папка")
elif not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'utils.log')
handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - utils - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def load_transactions(file_path):
    """Загружает транзакции из JSON-файла."""
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
        logger.info(f"Транзакции успешно загружены, количество: {len(transactions)}")
        return transactions
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        logger.error(f"Ошибка загрузки файла {file_path}: {e}")
        return []

def get_transaction_amount_rub(transaction):
    """Возвращает сумму транзакции в рублях."""
    logger.info("Начало конвертации суммы транзакции в рубли")
    if not isinstance(transaction, dict):
        logger.error(f"Transaction должен быть словарем, получено: {type(transaction)}")
        raise TypeError("Transaction must be a dictionary.")

    if 'operationAmount' not in transaction:
        logger.error("В транзакции отсутствует ключ 'operationAmount'")
        raise ValueError("Transaction must have 'operationAmount' key.")

    operation_amount = transaction['operationAmount']
    amount = operation_amount.get('amount')
    if amount is None:
        logger.error("В 'operationAmount' отсутствует ключ 'amount'")
        raise ValueError("Transaction must have 'amount' in 'operationAmount'")
    amount = float(amount)
    currency_dict = operation_amount.get('currency', {'code': 'RUB'})
    currency_code = currency_dict.get('code', 'RUB')

    logger.debug(f"Сумма: {amount}, валюта: {currency_code}")

    if currency_code != 'RUB':
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