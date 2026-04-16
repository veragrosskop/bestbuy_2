import products
from typing import List, Tuple


class Store:
    def __init__(self, product_list: List[products.Product]):
        """Initializes the store."""
        self.inventory = product_list

    def add_product(self, product: products.Product):
        """Adds a product to the store."""
        self.inventory.append(product)

    def remove_product(self, product: products.Product):
        """Removes a product from the store."""
        self.inventory.remove(product)

    def get_total_quantity(self) -> int:
        """Sums all the quantities of each product."""
        total = 0
        for product in self.inventory:
            if isinstance(product, products.NonStockedProduct):
                continue
            total += product.get_quantity()

        return total

    def get_all_products(self) -> List[products.Product]:
        """Returns a list of all products that are active"""

        active_products = [product for product in self.inventory if product.is_active()]
        return active_products

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        """Gets a list of tuples, where each tuple is:
        (product[product.Product], quantity[int])
        and buys the products and returns the total price of the order."""

        total_price = 0
        for item in shopping_list:
            product = item[0]
            quantity = item[1]

            if product in self.get_all_products():
                total_price += product.buy(quantity)
        return total_price
