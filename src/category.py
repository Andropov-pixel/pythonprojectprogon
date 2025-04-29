from typing import Any

from src.base import Base
from src.product import Product
from src.zero_product_exception import ZeroProductException


class Category(Base):
    """Категория товара"""

    category_count = 0
    product_count = 0

    name: str
    description: str
    products: list

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)
        print(Category.product_count)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."

    def add_product(self, product: Product) -> Any:
        if isinstance(product, Product):
            try:
                if product.quantity == 0:
                    raise ZeroProductException(
                        "Нельзя добавить товар с нулевым количеством"
                    )
            except ZeroProductException as e:
                print(str(e))
            else:
                self.__products.append(product)
                Category.product_count += 1
                print("Товар успешно добавлен")
            finally:
                print("Обработка добавления товара завершена")
        else:
            raise TypeError

    @property
    def get_product_list(self) -> str:
        product_list = ""
        for product in self.__products:
            product_list += f"{str(product)}\n"
        return product_list

    @property
    def products(self) -> list:
        products_list = []
        for product in self.__products:
            products_list.append(product)
        return products_list

    def middle_price(self):
        try:
            return sum(product.price for product in self.__products) / len(
                self.__products
            )
        except ZeroDivisionError:
            return 0


# result = Category("Product", "Description", ["product1", "product2", "product3"])
# print(result)