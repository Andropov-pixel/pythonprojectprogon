import pytest

from src.file_worker import FileWorker


def test_vacancy_is_str():
    """Пооверяем, что если название вакансии
    не является строкой, возникает ValueError"""
    with pytest.raises(ValueError):
        test_entity = FileWorker(123, "url",
                                 100000, "employer")

def test_salary_is_positive_number():
    """Пооверяем, что если зарплата
    не является числом, возвращается 0"""
    test_entity = FileWorker("Developer", "https://example.com/job123",
                             "salary", "employer")
    assert test_entity.salary == 0

def test_url_is_str():
    """Пооверяем, что если URL не является строкой,
     возникает ValueError"""
    with pytest.raises(ValueError):
        test_entity = FileWorker("EnergoTech", "url",
                                 100000, "employer")

def test_employer_is_str():
    """Пооверяем, что если название работодателя
    не является строкой, возникает ValueError"""
    with pytest.raises(ValueError):
        test_entity = FileWorker("EnergoTech", "https://example.com/job123",
                                 100000, 123)