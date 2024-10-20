from collections import Counter
from typing import Dict, List

from src.read_csv import get_csv_data_dict


def get_category_counter_by_description(
    dictionaries: List[Dict], operations: List
) -> Dict:
    """Принимает на вход список словарей с операциями
     и список строк с категориями, возвращает
    словарь, где ключи - категории, а значения - к
    оличество операций в этой категории"""
    operations_list = []
    counted = {}
    for dictionary in dictionaries:
        if dictionary["description"] in operations:
            operations_list.append(dictionary["description"])
        counted = Counter(operations_list)
    return counted


if __name__ == "__main__":
    dictionaries_1 = get_csv_data_dict("../data/transactions.csv")
    list_category: list[str] = [
        "Открытие вклада",
        "Перевод с карты на карту",
        "Перевод со счета на счет",
    ]
    result = get_category_counter_by_description(dictionaries_1, list_category)
    print(result)
