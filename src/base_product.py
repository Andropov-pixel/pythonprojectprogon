from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный класс для всех продуктов"""

    @classmethod
    @abstractmethod
    def new_product(cls, *args, **kwargs):
        pass
