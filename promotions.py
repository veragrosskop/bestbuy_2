import products
from typing import Optional
from abc import ABC, abstractmethod


class Promotion(ABC):
    """This class creates a promotion for a product."""

    @abstractmethod
    def apply_promotion(self, product: products.Product, quantity: int) -> float:
        """Applies a promotion to the product and returns the discounted price."""
        pass


class PercentDiscount(Promotion):
    """This class creates a percentage discount for a product."""

    def __init__(self, name: str, percent: float):
        self.name = name
        self.percentage = percent

    def apply_promotion(self, product: products.Product, quantity: int) -> float:
        """Applies a promotion to the product and returns the discounted price."""

        discounted_price = product.price * quantity * ((100 - self.percentage) / 100)
        return discounted_price

    def __str__(self):
        return self.name


class SecondHalfPrice(Promotion):
    """This class reduces the price for every second product by half."""

    def __init__(self, name: str):
        self.name = name

    def apply_promotion(self, product: products.Product, quantity: int) -> float:
        """Applies a promotion to the product and returns the discounted price."""

        half_priced = quantity // 2
        full_priced = quantity - half_priced
        discounted_price = (product.price * 0.5 * half_priced) + (product.price * full_priced)

        return discounted_price

    def __str__(self):
        return self.name


class ThirdOneFree(Promotion):
    """This class creates a buy two, get one free product promotion."""

    def __init__(self, name: str):
        self.name = name

    def apply_promotion(self, product: products.Product, quantity: int) -> float:
        """Applies a promotion to the product and returns the discounted price."""

        non_discounted_amount = quantity % 3
        discounted_amount = quantity - non_discounted_amount
        discounted_price = (product.price * ((2 * discounted_amount) / 3)) + (
            non_discounted_amount * product.price
        )

        return discounted_price

    def __str__(self):
        return self.name
