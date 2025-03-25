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
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []  # Возвращаем пустой список, если данные не являются списком

        return data
    except FileNotFoundError:
        return []  # Возвращаем пустой список, если файл не найден
    except json.JSONDecodeError:
        return [] # Возвращаем пустой список, если не удалось декодировать JSON
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []  # Возвращаем пустой список в случае неожиданной ошибки (лучше логировать!)

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