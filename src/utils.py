import json
import os
from external_api import convert_to_rub


def load_transactions(file_path):
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        list: Список словарей с данными о транзакциях. Возвращает пустой список,
              если файл пустой, содержит не список или не найден.
    """
    transactions = []
    try:
        if not os.path.exists(file_path):
            return transactions

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            transactions = data

    except (FileNotFoundError, json.JSONDecodeError):
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")

    return transactions





def load_transactions(file_path):
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        list: Список словарей с данными о транзакциях. Возвращает пустой список,
              если файл пустой, содержит не список или не найден.
    """
    transactions = []
    try:
        if not os.path.exists(file_path):
            return transactions

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            transactions = data

    except (FileNotFoundError, json.JSONDecodeError):
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")

    return transactions

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

    amount = transaction['operationAmount'].get('amount')
    currency = transaction['operationAmount'].get('currency', 'RUB')