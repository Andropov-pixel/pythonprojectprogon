from src.lawn_grass_product import LawnGrass
from src.product import Product
from src.smartphone_product import Smartphone


def test_mixin_print(capsys):
    Product(
        name="Product",
        description="Description of the product",
        price=84.50,
        quantity=10,
    )
    message = capsys.readouterr()
    assert (
        message.out.strip() == "Product(Product, Description of the product, 84.5, 10)"
    )


def test_mixin_print_sph(capsys):
    Smartphone(
        name="Iphone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
        efficiency=98.2,
        model="15",
        memory=512,
        color="Gray space",
    )
    message = capsys.readouterr()
    assert (
        message.out.strip() == "Smartphone(Iphone 15, 512GB, Gray space, 210000.0, 8)"
    )


def test_mixin_print_lg(capsys):
    LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )
    message = capsys.readouterr()
    assert (
        message.out.strip()
        == "LawnGrass(Газонная трава, Элитная трава для газона, 500.0, 20)"
    )