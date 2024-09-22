import csv
import json
import logging
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()
api_key = os.getenv("API_KEY")

logger = logging.getLogger('utils')
file_handler = logging.FileHandler('../tests/logs/utils.log')
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')


def get_transactions_dictionary(path: str) -> Any:
    """Принимает путь до JSON-файла
    и возвращает список словарей с данными
    о финансовых транзакциях"""
    try:
        logger.info("Getting transaction list starts")
        with open(path, "r", encoding="utf-8") as operations:
            try:
                transactions_data = json.load(operations)
                logger.info("Transactions list ready")
                return transactions_data
            except json.JSONDecodeError:
                logger.error("Decode error")
                transactions_data = []
                return transactions_data
    except FileNotFoundError:
        logger.error("File was not found")
        transactions_data = []
        return transactions_data


def get_transactions_dictionary_csv(csv_path: str) -> list[dict]:
    """Aункция пути до CSV-файла и возвращает список словарей с данными о финансовых транзакциях"""

    transaction_list = []
    try:
        with open(csv_path, encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            next(reader)
            for row in reader:
                if row:
                    id_, state, date, amount, currency_name, currency_code, from_, to, description = row
                    transaction_list.append(
                        {
                            "id": str(id_),
                            "state": state,
                            "date": date,
                            "operationAmount": {
                                "amount": str(amount),
                                "currency": {"name": currency_name, "code": currency_code},
                            },
                            "description": description,
                            "from": from_,
                            "to": to,
                        }
                    )
    except Exception:
        return []
    return transaction_list


def get_transactions_dictionary_excel(excel_path: str) -> list[dict]:
    """FAункция пути до EXCEL-файла и возвращает список словарей с данными о финансовых транзакциях"""

    transaction_list = []
    try:
        excel_data = pd.read_excel(excel_path)
        len_, b = excel_data.shape
        for i in range(len_):
            if excel_data["id"][i]:
                transaction_list.append(
                    {
                        "id": str(excel_data["id"][i]),
                        "state": excel_data["state"][i],
                        "date": excel_data["date"][i],
                        "operationAmount": {
                            "amount": str(excel_data["amount"][i]),
                            "currency": {
                                "name": excel_data["currency_name"][i],
                                "code": excel_data["currency_code"][i],
                            },
                        },
                        "description": excel_data["description"][i],
                        "from": excel_data["from"][i],
                        "to": excel_data["to"][i],
                    }
                )
            else:
                continue
    except Exception:
        return []
    return transaction_list


def transaction_amount_in_rub(transactions: list, transaction_id: int) -> Any:
    """Принимает транзакцию и возвращает сумму в рублях,
    если операция не в рублях, конвертирует"""
    logger.info("Getting operation amount starts")
    for transaction in transactions:
        if transaction.get("id") == transaction_id:
            if transaction["operationAmount"]["currency"]["code"] == "RUB":
                rub_amount = transaction["operationAmount"]["amount"]
                logger.info(f"Operation amount in RUB:{rub_amount}")
                return rub_amount
            else:
                transaction_convert = dict()
                transaction_convert["amount"] = (
                    transaction)["operationAmount"]["amount"]
                transaction_convert["currency"] = \
                    transaction["operationAmount"][
                        "currency"
                    ]["code"]
                logger.info(
                    f"Operation amount in "
                    f"{transaction_convert["currency"]}:"
                    f"{transaction_convert["amount"]}"
                )
                #                print(transaction_convert)
                rub_amount = round(convert_to_rub(transaction_convert), 2)
                if rub_amount != 0:
                    logger.info(f"Operation amount in RUB:{rub_amount}")
                    return rub_amount
                else:
                    logger.error("Operation amount can't be converted to RUB")
                    return "Конвертация не может быть выполнена"
    else:
        return "Транзакция не найдена"


def convert_to_rub(transaction_convert: dict) -> Any:
    amount = transaction_convert["amount"]
    currency = transaction_convert["currency"]
    """Принимает значение в долларах или евро,
     обращается к внешнему API и возвращает конвертацию в рубли"""
    try:
        if currency == "USD":
            url = (
                f"https://api.apilayer.com/exchangerates_data/"
                f"convert?to=RUB&from=USD&amount={amount}"
            )
            headers = {"apikey": api_key}
            response = requests.get(url, headers=headers)
            json_result = response.json()
            rub_amount = json_result["result"]
            return rub_amount
        elif currency == "EUR":
            url = (
                f"https://api.apilayer.com/exchangerates_data/"
                f"convert?to=RUB&from=EUR&amount={amount}"
            )
            headers = {"apikey": api_key}
            response = requests.get(url, headers=headers)
            json_result = response.json()
            rub_amount = json_result["result"]
            logger.info(f"Operation amount in USD/EUR in RUB:{rub_amount}")
            return rub_amount
    except RequestException:
        return 0

#    if __name__ == "utilts":
#    transactions = get_transactions_dictionary("../data/operations.json")
#    print(transaction_amount_in_rub(transactions, 41428829))
#     wine_reviews = pd.read_csv("transactions.csv")
#     excel_data = pd.read_excel("transactions_excel.xlsx")