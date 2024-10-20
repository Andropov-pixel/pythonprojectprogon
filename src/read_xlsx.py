from typing import Dict, List

import pandas as pd


def get_xlsx_data_dict(file_name: str) -> List[Dict]:
    """Считывает данные о финансовых операциях
    из excel файла и преобразует их в список словарей"""
    try:
        xlsx_data = pd.read_excel(file_name)
        data_list = xlsx_data.apply(
            lambda row: {
                "id": row["id"],
                "state": row["state"],
                "date": row["date"],
                "operationAmount": {
                    "amount": row["amount"],
                    "currency": {
                        "name": row["currency_name"],
                        "code": row["currency_code"],
                    },
                },
                "description": row["description"],
                "from": row["from"],
                "to": row["to"],
            },
            axis=1,
        )
        new_dict_list = []
        row_index = 0
        for _ in data_list:
            new_dict_list.append(data_list[row_index])
            row_index += 1
        return new_dict_list
    except Exception:
        return [{}]


# if __name__ == "__main__":
# result = get_xlsx_data_dict("../data/transactions_excel.xlsx")
# print(result)
