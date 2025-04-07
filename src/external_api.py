import json
import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


logging.basicConfig(
    level=logging.ERROR,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def convert_to_rub(amount, currency):
    """
    Конвертирует сумму из указанной валюты в рубли.

    Args:
        amount (float): Сумма для конвертации.
        currency (str): Валюта суммы (USD, EUR).

    Returns:
        float: Сумма в рублях.
        Возвращает None, если не удалось получить курс обмена.
    """
    if currency == "RUB":
        return amount

    if not API_KEY:
        raise ValueError("EXCHANGE_RATES_API_KEY is not set in environment variables.")

    url = f"{BASE_URL}?symbols=RUB&base={currency}"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if "rates" in data and "RUB" in data["rates"]:
            rub_rate = data["rates"]["RUB"]
            return amount * rub_rate
        else:
            # Логируем ошибку, прежде чем вернуть None
            logging.error(f"Could not retrieve RUB rate for {currency}. API response: {data}")
            return None  # Или raise ValueError, если отсутствие курса - это исключительная ситуация

    except requests.exceptions.RequestException as e:
        # Логируем ошибку API
        logging.error(f"API request failed: {e}")
        return None  # Или raise Exception, если ошибка запроса критична
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return None
