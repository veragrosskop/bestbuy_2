import pytest
from products import Product


def test_product_creation():
    product = Product("MacBook Air M2", price=10, quantity=100)
    assert product.price == 10
    assert product.get_quantity() == 100
    assert product.name == "MacBook Air M2"
    assert product.is_active() is True


def test_invalid_name():
    with pytest.raises(Exception, match="Product name is empty"):
        Product("", price=1450, quantity=100)


def test_invalid_price():
    with pytest.raises(Exception, match="Product price is negative"):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_inactive():
    product = Product("MacBook Air M2", price=10, quantity=100)
    assert product.is_active() is True
    product.buy(100)
    assert product.is_active() is False


def test_product_purchase():
    product = Product("MacBook Air M2", price=10, quantity=100)
    assert product.buy(10) == 100
    assert product.get_quantity() == 90
    assert product.buy(2) == 20
    assert product.get_quantity() == 88


def test_too_few_stock():
    product = Product("MacBook Air M2", price=10, quantity=100)
    with pytest.raises(Exception, match=f"There aren't enough MacBook Air M2's in storage. /n"):
        product.buy(110)
