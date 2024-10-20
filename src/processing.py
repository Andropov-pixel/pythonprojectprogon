from typing import Any

initial_list = [
    {"id": 41428829, "state": "EXECUTED",
     "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED",
     "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED",
     "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED",
     "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(
    initial_list: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Принимает на вход список словарей и возвращает новый список,
    содержащий только те словари, у которых ключ state содержит переданное
    в функцию значение."""
    result_list = []
    for num_list in initial_list:
        if num_list.get("state") == state:
            result_list.append(num_list)
    return result_list


def sort_by_date(
    initial_list: list[dict[str, Any]], reverse_list: bool = True
) -> list[dict[str, Any]]:
    """Принимает на вход список словарей и возвращает новый список,
    в котором исходные словари отсортированы по убыванию даты."""
    sorted_list = (sorted
                   (initial_list, key=lambda d: d["date"],
                    reverse=reverse_list))
    return sorted_list


print(filter_by_state(initial_list))
print(sort_by_date(initial_list))
