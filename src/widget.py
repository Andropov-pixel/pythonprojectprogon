from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_info: str) -> str:
    """принимает название и номер карты или номер счета
    и возвращает замаскированный номер
    :rtype: object"""
    payment_info = card_or_account_info.split(" ")
    payment_number = int(payment_info[-1])
    payment_name = payment_info[:-1]
    if card_or_account_info.lower().startswith("счет"):
        number = get_mask_account(payment_number)
    else:
        number = get_mask_card_number(payment_number)
    return " ".join(payment_name) + f" {number}"


def get_date(date_info: str) -> str:
    """преобразует дату в формат dd.mm.yy"""
    converted_date = datetime.fromisoformat(date_info).strftime("%d.%m.%Y")
    return converted_date


print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card("Visa Classic 6831982476737658"))
print(get_date("2018-07-11T02:26:18.671407"))
