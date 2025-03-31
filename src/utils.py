import json
import os
from external_api import convert_to_rub
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_transactions(file_path):
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        list: Список словарей с данными о транзакциях. Возвращает пустой список,
              если файл пустой, содержит не список или не найден.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []


def get_transaction_amount_rub(transaction):
    """
    Возвращает сумму транзакции в рублях.

    Args:
        transaction (dict): Словарь с данными о транзакции.

    Returns:
        float: Сумма транзакции в рублях.
    """
    if not isinstance(transaction, dict):
        raise TypeError("Transaction must be a dictionary.")

    if 'operationAmount' not in transaction:
        raise ValueError("Transaction must have 'operationAmount' key.")

    operation_amount = transaction['operationAmount']
    amount = float(operation_amount.get('amount', 0))
    currency_dict = operation_amount.get('currency', {'code': 'RUB'})  # По умолчанию RUB
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