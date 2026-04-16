from typing import List, Tuple
from unittest import case

import store
import products
import promotions


def ask_int_input(min_choices: int, max_choices: int):
    """ask user to enter integer input. Recursive function for user input."""
    choice = input("\nPlease choose a number: ")

    if choice == 0:  # return to main menu/finish order
        return 0
    elif choice == "":
        return 0
    elif choice.isdigit():
        choice = int(choice)
        if choice < min_choices or choice > max_choices:
            print(f"{choice} is not a valid integer in range {min_choices} to {max_choices}")
            return ask_int_input(min_choices, max_choices)
        else:
            return choice
    else:
        print(f"{choice} is not a valid integer in range {min_choices} to {max_choices}")
        return ask_int_input(min_choices, max_choices)


def order_menu(s: store.Store, shopping_list, subtotal) -> List[Tuple[products.Product, int]]:
    """Recursive function for order menu.
    Will recursively ask a user to choose a product and an order amount.
    Until the user presses enter to exit the menu twice.
    """

    print("When you want to finish order, enter empty text.\n" "Which product # do you want?")

    product_menu(s)
    # initialize updated inventory
    inventory = s.get_all_products()
    product_choice = ask_int_input(0, len(inventory))
    if product_choice == 0 or "":  # conclude order and exit to main menu
        return s, shopping_list, subtotal

    else:  # buy a product
        prod = inventory[product_choice - 1]
        if isinstance(prod, products.NonStockedProduct):
            available = 99999
        else:
            available = prod.get_quantity()
        reserved_amount = 0
        # check if you already added some of the product to the list
        if shopping_list:  # if there's already something in the shopping list
            for item in shopping_list:
                if item[0] == prod:
                    reserved_amount += item[1]

        print(f"How many do you want to add to your reservation of: {reserved_amount}.")
        if isinstance(prod, products.LimitedProduct):
            available = prod.get_available(reserved_amount)
            if available > 0:
                amount = ask_int_input(0, available)  # validate quantity and max buy
            else:
                amount = 0
        else:
            amount = ask_int_input(0, available - reserved_amount)  # validate quantity
        shopping_list.append((prod, amount))
        subtotal += s.order([(prod, amount)])
        print(f"--> Product: {prod.name}. Amount: {amount} added to list! subtotal is {subtotal}")

        return order_menu(s, shopping_list, subtotal)  # prompt for new product acquisition


def product_menu(s: store.Store):
    """List available products as a menu."""

    inventory = s.get_all_products()
    print("-----")
    for i in range(1, len(inventory) + 1):
        print(f"{i}. {inventory[i - 1]}")
    print("-----")


def start(s: store.Store):
    """Main menu of the store."""

    print(
        "Store Menu\n"
        "____________\n"
        "1. List all products in store\n"
        "2. Show total amount in store\n"
        "3. Make an order\n"
        "4. Quit"
    )
    choice = ask_int_input(1, 4)

    match choice:
        case 0:
            start(s)
        case 1:
            product_menu(s)
            start(s)
        case 2:
            quantity = s.get_total_quantity()
            print(f"Total of {quantity} items in store")
            start(s)
        case 3:
            s, shopping_list, total = order_menu(s, [], 0)  # generate the shopping list
            print(f"Order made! Total payment: {total}")
            start(s)
        case 4:
            print("Thank you for visiting.")
        case _:
            print("Please choose a number between 1-4")


if __name__ == "__main__":

    # setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)
    best_buy = store.Store(product_list)

    start(best_buy)
