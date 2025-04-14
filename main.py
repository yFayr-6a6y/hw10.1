from datetime import datetime
from typing import Dict, List

from src.utils import (
    load_transactions,
    get_transaction_amount_rub,
    filter_transactions_by_description,
    count_transactions_by_category,
)
from src.widget import get_date, mask_account_card


def format_transaction(transaction: Dict) -> str:
    """
    Форматирует транзакцию для вывода в консоль.

    Args:
        transaction (Dict): Словарь с данными о транзакции.

    Returns:
        str: Отформатированная строка с информацией о транзакции.
    """
    # Форматируем дату
    date_str = transaction.get("date", "")
    formatted_date = get_date(date_str)  # Используем get_date из widget.py

    description = transaction.get("description", "Описание отсутствует")


    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")
    if from_account and to_account:
        from_account = mask_account_card(from_account)  # Маскируем с помощью mask_account_card
        to_account = mask_account_card(to_account)
        from_to = f"{from_account} -> {to_account}"
    elif to_account:
        to_account = mask_account_card(to_account)
        from_to = to_account
    else:
        from_to = "Не указан"

    try:
        amount_rub = get_transaction_amount_rub(transaction)
        currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code", "RUB")
    except (ValueError, TypeError):
        amount_rub = transaction.get("operationAmount", {}).get("amount", 0)
        currency_code = "RUB"

    return f"{formatted_date} {description}\n{from_to}\nСумма: {amount_rub:.0f} {currency_code}\n"


def main():
    """
    Основная логика программы для работы с банковскими транзакциями.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input().strip()
    file_path = ""
    if file_choice == "1":
        file_path = "data/transactions.json"
        print("Для обработки выбран JSON-файл.")
    elif file_choice == "2":
        file_path = "data/transactions.csv"
        print("Для обработки выбран CSV-файл.")
    elif file_choice == "3":
        file_path = "data/transactions_excel.xlsx"
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Завершение программы.")
        return

    # Загружаем транзакции
    transactions = load_transactions(file_path)
    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    # Фильтрация по статусу
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().strip().upper()
        if status in available_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            transactions = [tx for tx in transactions if tx.get("state", "").upper() == status]
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_by_date = input().strip().lower()
    if sort_by_date == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        sort_order = input().strip().lower()
        reverse = sort_order != "по возрастанию"
        transactions.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    print("Выводить только рублевые транзакции? Да/Нет")
    rub_only = input().strip().lower()
    if rub_only == "да":
        transactions = [
            tx for tx in transactions
            if tx.get("operationAmount", {}).get("currency", {}).get("code", "") == "RUB"
        ]

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    filter_by_desc = input().strip().lower()
    if filter_by_desc == "да":
        print("Введите строку для поиска в описании:")
        search_string = input().strip()
        transactions = filter_transactions_by_description(transactions, search_string)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for transaction in transactions:
            print(format_transaction(transaction))

    categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада", "Перевод со счета на счет"]
    category_counts = count_transactions_by_category(transactions, categories)
    print("\nСтатистика по категориям:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()