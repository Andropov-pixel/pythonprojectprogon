import unittest
from unittest.mock import patch
import pytest

from src.parser import HH


class TestParser(unittest.TestCase):

    @patch('requests.get')
    def test_load_vacancies_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "items": [{"id": 1, "name": "Вакансия 1"}, {"id": 2, "name": "Вакансия 2"}]
        }

        # Создаем экземпляр класса HH
        hh_parser = HH()
        result = hh_parser.load_vacancies("python")

        # Проверяем, что метод вернул правильные вакансии
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Вакансия 1")
        self.assertEqual(result[1]["name"], "Вакансия 2")  # Проверяем название второй вакансии

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        mock_get.return_value.status_code = 404

        # Создаем экземпляр класса HH
        hh_parser = HH()
        result = hh_parser.load_vacancies("python")

        # Проверяем, что метод вернул []
        self.assertEqual(result, [])