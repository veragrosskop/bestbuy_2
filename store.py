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

    def get_all_available_products(self) -> List[products.Product]:
        """
        Returns a list of all products that are available and active.
        Compared to get_all_products, this will also take into account the reserved quantity.
        """

        active_products = [
            product
            for product in self.inventory
            if (product.is_active() and product.is_available())
        ]
        return active_products

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        """Gets a list of tuples, where each tuple is:
        (product[product.Product], quantity[int])
        and buys the products and returns the total price of the order."""

        total_price = 0
        bill = "\n==========================================="
        for product, quantity in shopping_list:
            if product.promotion:
                bill += self.format_promotion(product.promotion.name)
            product_price = product.buy(quantity)
            bill += self.format_bill_line(f"{product.name} x{quantity}", product_price)
            total_price += product_price
        bill += "\n==========================================="
        bill += self.format_bill_line("Total price", total_price)

        return total_price, bill

    def add_to_shoppinglist(
        self,
        single_order: Tuple[products.Product, int],
        shopping_list: List[Tuple[products.Product, int]],
    ) -> List[Tuple[products.Product, int]]:
        """
        Adds a product to the shopping list and ensures there are no double entries per product.
        If the product already has a quantity, the quantity will be incremented.
        """

        new_product = single_order[0]
        amount = single_order[1]
        for i, (product, quantity) in enumerate(shopping_list):
            if product == new_product:
                shopping_list[i] = (product, quantity + amount)
                break
        else:
            shopping_list.append((new_product, amount))

    def format_bill_line(self, product: str, price: float) -> str:
        """Formats a billing line for a product, with spacing and right justified price."""
        return "\n{:30s}{:>7s}".format(product, "${:.2f}".format(price))

    def format_promotion(self, promotion: str):
        """Formats a promotion line on the bill."""
        return "\n{:30s}{:>7s}".format(promotion, "")
