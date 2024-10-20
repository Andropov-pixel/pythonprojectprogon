import csv
from typing import Dict, List


def get_csv_data_dict(file_name: str) -> List[Dict]:
    """Считывает данные о финансовых операциях
    из CSV файла и преобразует их в список словарей"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            csv_data = csv.reader(file, delimiter=";")
            header = next(csv_data)
            list_new_dict = []
            for row in csv_data:
                row_new_dict = {
                    "id": row[header.index("id")],
                    "state": row[header.index("state")],
                    "date": row[header.index("date")],
                    "operationAmount": {
                        "amount": row[header.index("amount")],
                        "currency": {
                            "name": row[header.index("currency_name")],
                            "code": row[header.index("currency_code")],
                        },
                    },
                    "description": row[header.index("description")],
                    "from": row[header.index("from")],
                    "to": row[header.index("to")],
                }
                list_new_dict.append(row_new_dict)
            return list_new_dict
    except Exception:
        return [{}]


# if __name__ == "__main__":
#     result = get_csv_data_dict("../data/transactions.csv")
#     print(result)
