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

    def show(self):
        """Returns a string of product details: name, price, quantity."""
        return f"{self.name}, Price: {self.price}, Quantity: {self.__quantity}"

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
            new_quantity = self.__quantity - quantity
            self.set_quantity(new_quantity)
            total_price = self.price * quantity

            return total_price
        return None
