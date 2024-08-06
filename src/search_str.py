import re
from typing import Dict, List


def search_by_string(dictionaries: List[Dict], user_string: str) -> List[Dict]:
    """Принимеает список словарей и
    строку поиска, возвращает список словарей,
     у которых в описании есть эта строка"""
    new_dict_list = []
    for dictionary in dictionaries:
        text = dictionary["description"]
        needed = re.findall(user_string, text, flags=re.IGNORECASE)
        if needed:
            new_dict_list.append(dictionary)
    return new_dict_list


# if __name__ == "__main__":
#    dictionaries_1 = get_csv_data_dict("../data/transactions.csv")
#    result = search_by_string(dictionaries_1, "перевод")
#    print(result)
