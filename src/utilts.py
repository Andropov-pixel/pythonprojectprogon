import csv
import json
import logging
import os
from typing import Any
import datetime
import pandas as pd
import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()
api_key = os.getenv("API_KEY")
EXCHANGE_RATES_DATA_API = os.getenv("API_KEY_APILAYER")
API = os.getenv("API_KEY_ALPHA_VANTAGE")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR, "logs", "utils.log")

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
utils_logger = logging.getLogger("utils")


def top_5_transactions(date_string: str, data_frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция отображения топ 5 транзакций по сумме платежа"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_string_dt_obj.replace(day=1)
        edited_df = data_frame.drop(
            [
                "Payment date",
                "Card number",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "MCC",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_string_dt_obj)
            & (edited_df["Transaction date"] >= start_date_for_sorting)
            & (edited_df["Transaction amount"].notnull())
            & (edited_df["Status"] != "FAILED")
            ]
        sorted_df_by_transaction_amount = filtered_df_by_date.sort_values(
            by=["Transaction amount"], ascending=False, key=lambda x: abs(x)
        )
        top_transactions = sorted_df_by_transaction_amount[0:5]
        data_list = []
        for index, row in top_transactions.iterrows():
            data_dict = {
                "date": row["Transaction date"].strftime("%d.%m.%Y"),
                "amount": round(row["Transaction amount"], 2),
                "category": row["Category"],
                "description": row["Description"],
            }
            data_list.append(data_dict)
        utils_logger.info("Данные по топу транзакций успешно сформированны")
    except ValueError:
        utils_logger.error("Ошибка ввода данных: неверный формат даты")
        print("Неверный формат даты")
        return []
    else:
        return data_list


def card_info(date_string: str, data_frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция отображения информации о карте в заданном формате"""
    try:
        date_string_dt_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_string_dt_obj.replace(day=1)
        edited_df = data_frame.drop(
            [
                "Payment date",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "Category",
                "MCC",
                "Description",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_string_dt_obj)
            & (edited_df["Transaction date"] >= start_date_for_sorting)
            & (edited_df["Card number"].notnull())
            & (edited_df["Transaction amount"] <= 0)
            & (edited_df["Status"] != "FAILED")
            ]
        grouped_df = filtered_df_by_date.groupby(["Card number"], as_index=False).agg({"Transaction amount": "sum"})
        grouped_df["cashback"] = grouped_df["Transaction amount"].apply(lambda x: round(abs(x) / 100, 2))
        grouped_df["Card number"] = grouped_df["Card number"].apply(lambda x: x.replace("*", ""))
        data_list = grouped_df.to_dict("records")
        utils_logger.info("Данные по картам успешно сформированны")
        return data_list
    except ValueError:
        print("Неверный формат даты")
        utils_logger.error("Ошибка ввода данных: неверный формат даты")
        return []


def share_price(stock_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получающая курс акций"""
    stocks_rate = []
    for stock in stock_list:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API}"
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            date = res["Meta Data"]["3. Last Refreshed"]
            new_dict = {"stock": stock, "price": round(float(res["Time Series (Daily)"][f"{date}"]["2. high"]), 2)}
            stocks_rate.append(new_dict)
        else:
            utils_logger.info("Произошла ощибка")
            print("Произошла ошибка")
    utils_logger.info("Данные по курсу акций успешно получены")
    return stocks_rate


def greeting():
    """Функция вывода сообщения приветствия в зависимости от времени суток"""
    opts = {"greeting": ("Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи")}
    current_time = datetime.datetime.now()
    if 4 <= current_time.hour <= 12:
        greet = opts["greeting"][0]
    elif 12 <= current_time.hour <= 16:
        greet = opts["greeting"][1]
    elif 16 <= current_time.hour <= 24:
        greet = opts["greeting"][2]
    else:
        greet = opts["greeting"][3]
    return greet


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


def exchange_rate(currency_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получения курса валют через API"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": f"{EXCHANGE_RATES_DATA_API}"}
    currency_rate = []
    for currency in currency_list:
        payload = {"symbols": "RUB", "base": f"{currency}"}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            currency_rate_dict = {"currency": f"{res["base"]}", "rate": round(float(res["rates"]["RUB"]), 2)}
            currency_rate.append(currency_rate_dict)
        else:
            print("Запрос не был успешным.")
            utils_logger.warning("Запрос не удался")
            return []
    utils_logger.info("Данные по курсу валют успешно получены")
    return currency_rate


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
