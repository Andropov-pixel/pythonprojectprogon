from typing import Any, Dict, List

from src.utilts import get_transactions_dictionary
from src.read_csv import get_csv_data_dict
from src.read_xlsx import get_xlsx_data_dict
from src.processing import filter_by_state, sort_by_date
from src.format_output import get_right_format
from src.search_str import search_by_string

print("Привет! Добро пожаловать" " "
      "в программу" "работы с банковскими транзакциями.")

print(
    "Выберите необходимый пункт меню:"
    "\n1. Получить информацию о транзакциях из JSON-файла"
    "\n2. Получить информацию о транзакциях из CSV-файла"
    "\n3. Получить информацию о транзакциях из XLSX-файла"
)

user_input = input()

while True:
    if user_input == "1":
        print("Для обработки выбран JSON-файл")
        break
    elif user_input == "2":
        print("Для обработки выбран CSV-файл")
        break
    elif user_input == "3":
        print("Для обработки выбран XLSX-файл")
        break
    else:
        print(
            "Вы не выбрали файл. Выберите необходимый файл: "
            "\n1. Получить информацию о транзакциях из JSON-файла "
            "\n2. Получить информацию о транзакциях из CSV-файла "
            "\n3. Получить информацию о транзакциях из XLSX-файла"
        )
        user_input = input()


def get_transactions(user_input: str) -> Any:
    """Выбирает нужный путь к файлу в выбранном формате"""
    if user_input == "1":
        transactions = get_transactions_dictionary("../data/operations.json")
        return transactions
    elif user_input == "2":
        transactions = get_csv_data_dict("../data/transactions.csv")
        return transactions
    elif user_input == "3":
        transactions = get_xlsx_data_dict("../data/transactions_excel.xlsx")
        return transactions


transactions_step_1 = get_transactions(user_input)
# print(transactions_step_1)
print(
    "Введите статус, по которому необходимо выполнить фильтрацию. "
    "\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
)
user_input_2 = input()

while True:
    if user_input_2.lower() == "executed":
        print("Операции отфильтрованы по статусу EXECUTED")
        break
    elif user_input_2.lower() == "canceled":
        print("Операции отфильтрованы по статусу CANCELED")
        break
    elif user_input_2.lower() == "pending":
        print("Операции отфильтрованы по статусу PENDING")
        break
    else:
        print(f"Статус операции {user_input_2} недоступен")
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        user_input_2 = input()

transactions_step_2 = filter_by_state(transactions_step_1, user_input_2)
# print(transactions_step_2)

print("Отсортировать операции по дате? Да/Нет")
user_input_3 = input()

if user_input_3.lower() == "да":
    print("Отсортировать по возрастанию или по убыванию?")
    user_input_4 = input()
    if (
        user_input_4.lower() != "по возрастанию"
        and user_input_4.lower() != "по убыванию"
    ):
        print("Введите: по возрастанию / по убыванию")
        user_input_4 = input()
elif user_input_3.lower() != "да":
    user_input_4 = ""


def get_transactions_list_by_date(
    transactions: List[Dict], user_input: str, user_input_sort: str
) -> Any:
    """сортировка по дате транзакции"""
    if user_input.lower() == "да":
        if user_input_sort.lower() == "по возрастанию":
            new_transactions = sort_by_date(transactions, True)
            return new_transactions
        elif user_input_sort.lower() == "по убыванию":
            new_transactions = sort_by_date(transactions, False)
            return new_transactions
    elif user_input.lower() != "да":
        return transactions


transactions_step_3 = get_transactions_list_by_date(
    transactions_step_2, user_input_3, user_input_4
)
# print(transactions_step_3)

print("Выводить только рублевые транзакции? Да/Нет")
user_input_5 = input()


def get_transactions_list_rub(transactions: List[Dict],
                              user_input: str) -> Any:
    new_transactions = []
    if user_input.lower() == "да":
        for transaction in transactions:
            if transaction["operationAmount"]["currency"]["code"] == "RUB":
                new_transactions.append(transaction)
                return new_transactions
    else:
        return transactions


transactions_step_4 =\
    (get_transactions_list_rub
     (transactions_step_3, user_input_5))


print("Отфильтровать список транзакций " ""
      "по определенному слову в описании? Да/Нет")
user_input_6 = input()

if user_input_6.lower() == "да":
    print("Введите слово:")
    user_input_7 = input()
elif user_input_6.lower() != "да":
    user_input_7 = ""


def get_transactions_list_by_word(
    transactions: List[Dict], user_input: str, word: str
) -> Any:
    """По необходимости возвращает только операции,
    в описании которых есть введенное слово"""
    if user_input.lower() == "да":
        new_transactions = search_by_string(transactions, word)
        return new_transactions
    elif user_input.lower() != "да":
        return transactions


transactions_step_5 = get_transactions_list_by_word(
    transactions_step_4, user_input_6, user_input_7
)
# print(transactions_step_5)

print("Распечатываю итоговый список транзакций...")

result = get_right_format(transactions_step_5)
print(result)

# python3 main/widget.py
