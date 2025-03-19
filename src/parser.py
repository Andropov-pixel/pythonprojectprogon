from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """Создаем абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def _connect_to_api(self, keyword):
        """Абстрактный метод для подключения к API"""
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        """Абстрактный метод для получения вакансий по ключевому слову"""
        pass


class HH(Parser):
    """Подключается к API HH и получает вакансии по ключевому слову"""

    def _connect_to_api(self, keyword):
        """Приватная функция подключения к API"""
        url = "https://api.hh.ru/vacancies"
        params = {"text": keyword, "per_page": 20}
        # Параметры запроса: ключевое слово и количество вакансий на странице
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Произошла ошибка: {response.status_code}")
            return None
        data = response.json()
        return data

    def load_vacancies(self, keyword=""):
        """Функция получает вакансии по ключевому слову"""
        data = self._connect_to_api(keyword)
        if data and "items" in data:
            # Проверяем, что ключ 'items' существует в ответе
            return data["items"]
        else:
            return []  # Если вакансий нет, возвращаем пустой список