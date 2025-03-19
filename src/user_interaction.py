from src.parser import HH
from src.utils import (
    print_search_query,
    search_by_query_desc,
    sort_vacancies_by_top_salary,
)


def interact():
    choice = input(
        "Приветствуем вас!\n"
        "Выберите нужное действие и введите его номер.\n"
        "1. Поиск вакансий на HH.ru по ключевому слову\n"
        "2. Топ вакансий по зарплате\n"
        "3. Поиск вакансий по ключевому слову в описании\n"
        "Ваш выбор: "
    )
    if choice not in ("1", "2", "3"):
        print("Неверный выбор. Программа завершает работу.")
        return
    if choice == "1":
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies = HH().load_vacancies(keyword)
        print_search_query(vacancies, keyword)
    elif choice == "2":
        n = int(
            input(
                "Укажите, сколько вакансий с "
                "максимальной зарплатой вы хотите увидеть: "
            )
        )
        vacancies = HH().load_vacancies()
        sort_vacancies_by_top_salary(vacancies, n)
    elif choice == "3":
        desc_keyword = input("Введите ключевое слово для поиска в описаниях: ")
        vacancies = HH().load_vacancies()
        search_by_query_desc(desc_keyword, vacancies)


# if __name__ == "__main__":
#     interact()