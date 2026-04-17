import pytest
import products
import promotions


@pytest.fixture
def product():
    return products.Product("Test Product", price=100, quantity=100)


# -------------------
# PercentDiscount
# -------------------


def test_percent_discount_basic(product):
    promo = promotions.PercentDiscount("10% off", 10)
    assert promo.apply_promotion(product, 2) == 180


def test_percent_discount_zero(product):
    promo = promotions.PercentDiscount("0%", 0)
    assert promo.apply_promotion(product, 3) == 300


def test_percent_discount_thirty(product):
    promo = promotions.PercentDiscount("30%", 30)
    assert promo.apply_promotion(product, 1) == 70


def test_percent_discount_full(product):
    promo = promotions.PercentDiscount("100%", 100)
    assert promo.apply_promotion(product, 5) == 0


# -------------------
# SecondHalfPrice
# -------------------


def test_second_half_price_even(product):
    promo = promotions.SecondHalfPrice("Second half")
    # 4 items → 2 full + 2 half = 100 + 100 + 50 + 50 = 300
    assert promo.apply_promotion(product, 4) == 300


def test_second_half_price_odd(product):
    promo = promotions.SecondHalfPrice("Second half")
    # 3 items → 2 full + 1 half = 100 + 100 + 50 = 250
    assert promo.apply_promotion(product, 3) == 250


def test_second_half_price_single(product):
    promo = promotions.SecondHalfPrice("Second half")
    assert promo.apply_promotion(product, 1) == 100


# -------------------
# ThirdOneFree
# -------------------


def test_third_one_free_exact(product):
    promo = promotions.ThirdOneFree("3rd free")
    assert promo.apply_promotion(product, 3) == 200


def test_third_one_free_multiple(product):
    promo = promotions.ThirdOneFree("3rd free")
    assert promo.apply_promotion(product, 6) == 400


def test_third_one_free_with_remainder(product):
    promo = promotions.ThirdOneFree("3rd free")
    # 5 → pay for 4
    assert promo.apply_promotion(product, 5) == 400


def test_third_one_free_less_than_three(product):
    promo = promotions.ThirdOneFree("3rd free")
    assert promo.apply_promotion(product, 2) == 200
