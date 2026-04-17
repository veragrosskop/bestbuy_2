import promotions


class Product:

    def __init__(self, name: str, price: float, quantity: int):
        """This function creates a new product."""
        if not name:
            raise Exception("Product name is empty")
        else:
            self.name = name

        if price < 0:
            raise Exception("Product price is negative")
        else:
            self.price = price

        if quantity < 0:
            raise Exception("Product quantity is negative")
        else:
            self.__quantity = quantity

        self.__active = self.__quantity > 0  # deactivate if <0
        self.promotion = None
        self._reserved = 0

    def get_reserved(self) -> int:
        """Returns the reserved quantity of the product."""
        return self._reserved

    def get_available(self) -> int:
        """Returns the available quantity of the product."""
        return self.__quantity - self._reserved

    def is_available(self) -> bool:
        """Returns whether the product is available taking into account the reserved quantity."""
        return (self.get_available() > 0) and self.is_active()

    def reserve(self, quantity: int):
        """Reserves the quantity of the product."""
        if quantity > self.get_available():
            raise Exception(f"Not enough available {self.name} to reserve")
        self._reserved += quantity

    def unreserve(self, quantity: int):
        self._reserved -= quantity
        if self._reserved < 0:
            self._reserved = 0

    def get_quantity(self) -> int:
        """Returns the quantity of the product."""
        return self.__quantity

    def set_quantity(self, quantity: int):
        """This function sets the quantity of the product.
        If the quantity is less than 0, it will deactivate the product."""
        self.__quantity = quantity
        if self.__quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Getter for the active attribute."""
        return self.__active

    def activate(self):
        """This function activates the product."""
        self.__active = True

    def deactivate(self):
        """This function deactivates the product."""
        self.__active = False

    def set_promotion(self, promotion: promotions.Promotion) -> None:
        """This function sets the promotion attribute."""
        self.promotion = promotion

    def __str__(self):
        """Returns a string of product details: name, price, quantity."""
        return f"{self.name}, Price: {self.price}, Quantity: {self.__quantity}, Promotion: {self.promotion}"

    def buy(self, quantity: int) -> float:
        """This function buys a given quantity. It checks if that quantity is available.
        If it's available it returns the purchase price and updates the quantity of the product.
        """

        if quantity > self.__quantity:
            raise Exception(
                f"There aren't enough {self.name}'s in storage. /n"
                f"You need: {quantity}, but there's only: {self.__quantity}"
            )
        elif quantity < 0:
            raise Exception(f"There aren't enough {self.name}'s in storage. /n")
        else:
            self.unreserve(quantity)
            new_quantity = self.__quantity - quantity
            self.set_quantity(new_quantity)

            if self.promotion:
                total_price = self.promotion.apply_promotion(self, quantity)
            else:
                total_price = self.price * quantity

            return total_price


class NonStockedProduct(Product):
    """This class creates a non-stocked product.
    This is a product type for which the quantity will always remain 0. For example a license."""

    def __init__(self, name: str, price: float):
        super().__init__(name=name, price=price, quantity=0)
        super().activate()

    def reserve(self, quantity: int):
        """Reserves the quantity of the product."""
        self._reserved += quantity

    def buy(self, quantity: int) -> float:
        """Overwrites the buy function of Product to not change the product quantity."""

        self.unreserve(quantity)
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        return total_price

    def is_available(self) -> bool:
        """
        Returns whether the product is available taking into account the reserved quantity.
        For the NonStockedProduct this is always True, unless the product is deactivated.
        """
        return self.is_active()

    def get_available(self) -> str:
        """
        Returns the available quantity of the product.
        The amount is technically infinite.
        """

        return "infinite"

    def __str__(self):
        """Returns a string of product details: name, price"""

        return f"{self.name}, Price: {self.price}, Promotion: {self.promotion}"


class LimitedProduct(Product):
    """This class creates a limited product. These products are can only be added once per order."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name=name, price=price, quantity=quantity)
        self.__maximum = maximum

    def get_maximum(self) -> int:
        """Returns the maximum quantity of the product."""
        return self.__maximum

    def get_available(self) -> int:
        """Checks if the product can be purchased based on the current reserved quantity."""

        if self._reserved >= self.__maximum:
            available = 0
            print(
                f"You have already purchased the maximum of {self.get_maximum()} amount of {self.name}"
            )
        else:
            available = super().get_quantity() - self._reserved
            available = min(available, self.__maximum - self._reserved)
            if available == 0:
                print(
                    f"You have already purchased the maximum of {self.get_maximum()} amount of {self.name}"
                )
        return available

    def buy(self, quantity: int) -> float:
        """Overwrites the buy function of NonStockedProduct to enforce the maximum buy quantity."""

        if quantity > self.__maximum:
            raise Exception(
                f"A maximum amount of {self.__maximum} can be bought of {super().name}. /n"
            )
        else:
            return super().buy(quantity)

    def __str__(self):
        """Returns a string of product details: name, price, quantity, maximum purchase quantity"""

        return f"{self.name}, Price: {self.price}, Quantity: {super().get_quantity()}, Maximum Purchase Quantity: {self.__maximum}, Promotion: {self.promotion}"
