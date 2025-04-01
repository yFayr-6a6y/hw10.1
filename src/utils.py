import json
import logging
from .external_api import convert_to_rub

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_transactions(file_path):
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        logging.error(f"Ошибка загрузки файла {file_path}: {e}")
        return []

def get_transaction_amount_rub(transaction):
    """Возвращает сумму транзакции в рублях."""
    if not isinstance(transaction, dict):
        raise TypeError("Transaction must be a dictionary.")

    if 'operationAmount' not in transaction:
        raise ValueError("Transaction must have 'operationAmount' key.")

    operation_amount = transaction['operationAmount']
    amount = operation_amount.get('amount')
    if amount is None:
        raise ValueError("Transaction must have 'amount' in 'operationAmount'")
    amount = float(amount)
    currency_dict = operation_amount.get('currency', {'code': 'RUB'})
    currency_code = currency_dict.get('code', 'RUB')

    logging.debug(f"get_transaction_amount_rub: amount={amount}, currency={currency_code}")

    if currency_code != 'RUB':
        logging.info(f"Converting {amount} {currency_code} to RUB")
        converted_amount = convert_to_rub(amount, currency_code)
        if converted_amount is None:
            logging.error(f"Conversion failed for {amount} {currency_code}")
            raise ValueError(f"Could not convert {currency_code} to RUB")
        logging.info(f"Converted amount: {converted_amount} RUB")
        return converted_amount
    else:
        logging.info(f"Transaction already in RUB: {amount}")
        return amount