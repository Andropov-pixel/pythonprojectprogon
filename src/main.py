import os

from src.filter_by_word import str_sort
from src.generators import filter_by_currency
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utilts import get_transactions_dictionary, get_transactions_dictionary_csv, get_transactions_dictionary_excel
from src.product_category import *

PATH_TO_FILE_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
PATH_TO_FILE_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "transactions.csv")
PATH_TO_FILE_EXCEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "transactions_excel.xlsx")

# if __name__ == "__main__":
product1 = Product(
    "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
)
product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

category1 = Category(
    "Смартфоны",
    "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    [product1, product2, product3],
)

print(category1.products)
product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
category1.add_product(product4)
print(category1.products)
print(category1.product_count)

new_product = Product.new_product(
    {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
)
print(new_product.name)
print(new_product.description)
print(new_product.price)
print(new_product.quantity)

new_product.price = 800
print(new_product.price)

new_product.price = -100
print(new_product.price)
new_product.price = 0
print(new_product.price)


def main():
    """Main function of the Project."""

    while True:
        menu_item = input(
            """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
"""
        )
        if menu_item == "1":
            print("Для обработки выбран JSON-файл.")
            transactions = get_transactions_dictionary(PATH_TO_FILE_JSON)
            break
        elif menu_item == "2":
            print("Для обработки выбран CSV-файл.")
            transactions = get_transactions_dictionary_csv(PATH_TO_FILE_CSV)
            break
        elif menu_item == "3":
            print("Для обработки выбран XLSX-файл.")
            transactions = get_transactions_dictionary_excel(PATH_TO_FILE_EXCEL)
            break
        else:
            print("Такого пункта в меню нет, попробуйте еще раз.")

    state_list = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        state = input(
            """Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING.
"""
        ).upper()

        if state not in state_list:
            print(f'Статус операции "{state}" недоступен.')
        else:
            break

    filtered_transactions = filter_by_state(transactions, state)

    date_sort = input("Отсортировать операции по дате? Да/Нет. ").lower()
    if date_sort == "да":
        if input("Отсортировать по возрастанию или по убыванию? ").lower() == "по возрастанию":
            date_flag = False
        else:
            date_flag = True
        filtered_transactions = sort_by_date(filtered_transactions, date_flag)

    filter_by_rub = input("Выводить только рублевые транзакции? Да/Нет ")
    if filter_by_rub.lower() == "да":
        rub_transactions = filter_by_currency(filtered_transactions, "RUB")
        filtered_transactions = list(rub_transactions)[:-1]

    filter_by_word = input("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет ")
    if filter_by_word.lower() == "да":
        word = input("Введите слово: ")
        filtered_transactions = str_sort(filtered_transactions, word)
    #     for operation in filtered_transactions:
    #         if re.search(word, operation.get("description", "")):
    #             found_operations.append(operation)
    #             filtered_transactions = filter_by_rub(filtered_transactions, word)

    print("Распечатываю итоговый список транзакций...")
    if len(filtered_transactions) == 0:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for tr in filtered_transactions:
            tr_date = get_mask_account(tr["date"])
            currency = tr["operationAmount"]["currency"]["name"]
            if tr["description"] == "Открытие вклада":
                from_to = get_mask_card_number(tr["to"])
            else:
                from_to = get_mask_card_number(tr["from"]) + " -> " + get_mask_card_number(tr["to"])

            amount = tr["operationAmount"]["amount"]
            print(
                f"""{tr_date} {tr['description']}
{from_to}
Сумма: {round(float(amount))} {currency}
"""
            )


if __name__ == "__main__":
    main()
