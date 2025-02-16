from src.product import Product


def test_product(first_product, second_product):
    assert first_product.name == "Product"
    assert first_product.description == "Description of the product"
    assert first_product.price == 84.50
    assert first_product.quantity == 10

    assert second_product.name == "Product number two"
    assert second_product.description == "Description of the product number two"
    assert second_product.price == 155.87
    assert second_product.quantity == 34


def test_new_product(product_dict):
    product4 = Product.new_product(product_dict)
    assert product4.name == "Product 4"
    assert product4.description == "Description of the product 4"
    assert product4.price == 145.75
    assert product4.quantity == 23


def test_prod_price_property(capsys, first_product):
    first_product.price = -756.57
    message = capsys.readouterr()
    assert message.out.strip() == "Цена не должна быть нулевая или орицательная"
    first_product.price = 756.57
    assert first_product.price == 756.57


def test_product_str(first_product):
    assert str(first_product) == "Product, 84.5 руб. Остаток: 10 шт."


def test_product_add(first_product, second_product):
    assert first_product + second_product == 6144.58