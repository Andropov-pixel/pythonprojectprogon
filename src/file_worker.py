class FileWorker:
    """Создаем класс для работы с вакансиями. В этом классе нужно
    определить атрибуты, такие как название вакансии, ссылка на вакансию,
    зарплата, краткое описание или требования и т. п. (всего не менее
    четырех атрибутов). Класс должен поддерживать методы сравнения
    вакансий между собой по зарплате и валидировать данные, которыми
    инициализируются его атрибуты."""

    __slots__ = ["name", "url", "salary", "employer"]
    # Ограничение атрибутов для экономии памяти

    def __init__(self, name: str, url: str, salary: int, employer: str):
        self.name = self._validate_name(name)
        self.url = self._validate_url(url)
        self.salary = self._validate_salary(salary)
        self.employer = self._validate_employer(employer)

    def _validate_name(self, name):
        """Проверяет, что название вакансии является строкой."""
        if not isinstance(name, str):
            raise ValueError("Название вакансии должно быть строкой.")
        return name

    def _validate_url(self, url):
        """Проверяет, что ссылка на вакансию является
        строкой и начинается с "http"."""
        if not isinstance(url, str) or not url.startswith("http"):
            raise ValueError(
                "Ссылка на вакансию должна быть " 'строкой и начинаться с "http".'
            )
        return url

    def _validate_salary(self, salary):
        """Проверяет, что зарплата является числом и не
        отрицательной. Если нет, возвращает 0."""
        if not isinstance(salary, (int, float)) or salary < 0:
            return 0  # Если зарплата не указана или отрицательная, ставим 0
        return salary  # Возвращаем корректное значение

    def _validate_employer(self, employer):
        """Проверяет, что имя работодателя является непустой строкой."""
        if not isinstance(employer, str) or not employer.strip():
            raise ValueError("Имя работодателя должно быть строкой.")
        return employer

    def __lt__(self, other):
        """Магический метод, возвращающий True, если
        зарплата текущей вакансии меньше зарплаты другой вакансии."""
        return self.salary < other.salary

    def __gt__(self, other):
        """Магический метод, возвращающий True,
        если зарплата текущей вакансии больше зарплаты другой вакансии."""
        return self.salary > other.salary

    def __eq__(self, other):
        """Магический метод, возвращающий True, если зарплата
        текущей вакансии равна зарплате другой вакансии."""
        return self.salary == other.salary

    def __le__(self, other):
        """Магический метод, возвращающий True, если зарплата
        текущей вакансии меньше или равна зарплате другой вакансии."""
        return self.salary <= other.salary

    def __ge__(self, other):
        """Магический метод, возвращающий True, если зарплата
        текущей вакансии больше или равна зарплате другой вакансии."""
        return self.salary >= other.salary

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return (
            f"FileWorker(name={self.name}, url={self.url}, "
            f"salary={self.salary}, employer={self.employer})"
        )