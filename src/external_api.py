import os

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def convert_to_rub(transaction: dict, API_KEY=None) -> float:
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return float(amount)
    else:
        response = requests.get(
            f"https://api.apilayer.com/exchangerates_data/"
            f"convert?to=RUB&from={currency}&amount={amount}",
            headers={"apikey": API_KEY}
        )
        data = response.json()
        return float(data["result"])


"""Функция принимает значение в долларах,
    обращается к API и возвращает конвертацию в рубли/"""
