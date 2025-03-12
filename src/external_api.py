import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env

API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"

def convert_to_rub(amount, currency):
    """
    Конвертирует сумму из указанной валюты в рубли.

    Args:
        amount (float): Сумма для конвертации.
        currency (str): Валюта суммы (USD, EUR).

    Returns:
        float: Сумма в рублях.
    """
    if currency == 'RUB':
        return amount

    if not API_KEY:
        raise ValueError("EXCHANGE_RATES_API_KEY is not set in environment variables.")

    url = f"{BASE_URL}?symbols=RUB&base={currency}"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'rates' in data and 'RUB' in data['rates']:
            rub_rate = data['rates']['RUB']
            return amount * rub_rate
        else:
            raise ValueError(f"Could not retrieve RUB rate for {currency}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")