from src.base import Base
from src.product import Product


class Order(Base):
    product: str
    quantity: int
    total_price: float

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.total_price = self.get_total_price()

    def __str__(self):
        return f"Ваш заказ: {self.product.name}, {self.quantity} шт. на сумму {self.total_price} руб."

    def get_total_price(self):
        price = product.price
        total_price = price * self.quantity
        return total_price


if __name__ == "__main__":
    product = Product(
        name="Product",
        description="Description of the product",
        price=84.50,
        quantity=10,
    )
    order = Order(product, 5)
    result = order.__str__()
    print(result)
