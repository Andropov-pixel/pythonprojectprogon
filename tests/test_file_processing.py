import json

from src.file_processing import JSON_Processing


def test_add_vacancy(sample_vacancy, tmp_path):
    """Тест добавления вакансии в JSON"""
    test_file = tmp_path / "vacancies.json"  # Временный JSON-файл
    processor = JSON_Processing(str(test_file))

    # Добавляем вакансию
    processor.add_vacancy(sample_vacancy)

    # Читаем JSON и проверяем
    with open(test_file, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["name"] == "Python Developer"
    assert data[0]["url"] == sample_vacancy["url"]

def test_add_identical_vacancy(capsys, sample_vacancy, tmp_path):
    """Тест добавления дублирующейся вакансии в JSON"""
    test_file = tmp_path / "vacancies.json"  # Временный JSON-файл
    processor = JSON_Processing(str(test_file))

    # Добавляем вакансию
    processor.add_vacancy(sample_vacancy)

    # Добавляем вакансию еще раз
    processor.add_vacancy(sample_vacancy)

    # Проверяем сообщение об ошибке
    message=capsys.readouterr()
    assert message.out.strip() == ("Вакансия с url "
                                   "https://example.com/job123 уже существует.")