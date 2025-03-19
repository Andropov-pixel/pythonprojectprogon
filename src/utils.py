import json


def print_search_query(vacancies, keyword):
    filtered_vacancies = []
    for vacancy in vacancies:
        if keyword.lower() in vacancy["name"].lower():
            filtered_vacancies.append(vacancy)
    print(json.dumps(filtered_vacancies, indent=4, ensure_ascii=False))


def sort_vacancies_by_top_salary(vacancies, n):
    sorted_vacancies = sorted(
        vacancies,
        key=lambda v: (
            (v.get("salary", {}).get("to") or v.get("salary", {}).get("from") or 0)
            if isinstance(v.get("salary"), dict)
            else 0
        ),
        reverse=True,
    )
    top_vacancies = sorted_vacancies[:n]
    print(f"Топ {n} вакансий по зарплате:")
    for vacancy in top_vacancies:
        print(f"Вакансия: {vacancy['name']}")
        print(f"Зарплата: {vacancy.get('salary', 'Не указана')}")
        print()


def search_by_query_desc(desc_keyword, vacancies):
    filtered_desc_list = []
    for vacancy in vacancies:
        description = vacancy.get("description", "")
        if desc_keyword.lower() in description.lower():
            filtered_desc_list.append(vacancy)
    # Печать найденных вакансий
    if filtered_desc_list:
        for vacancy in filtered_desc_list:
            print(f"Вакансия: {vacancy['name']}")
            print(f"Описание: {vacancy['description']}")
            print()
    else:
        print("Вакансии с таким ключевым словом в описании не найдены.")