from typing import List, Tuple
import store
import products
import promotions


def ask_int_input(min_choices: int, max_choices: int | str):
    """ask user to enter integer input. Recursive function for user input."""

    choice = input("\nPlease choose a number: ")

    if choice == 0:  # return to main menu/finish order
        return 0
    elif choice == "":
        return 0
    elif choice.isdigit():
        choice = int(choice)
        try:
            max_choices = int(max_choices)  # check if it's an integer or "infinite"
            if choice < min_choices or choice > max_choices:
                print(f"{choice} is not a valid integer in range {min_choices} to {max_choices}")
                return ask_int_input(min_choices, max_choices)
            else:
                return choice
        except ValueError:
            # it was "infinite"
            if choice < min_choices:
                print(f"{choice} is not a valid integer in range {min_choices} to infinite")
                return ask_int_input(min_choices, max_choices)
            else:
                return choice
    else:
        print(f"{choice} is not a valid integer in range {min_choices} to {max_choices}")
        return ask_int_input(min_choices, max_choices)


def order_menu(s: store.Store, shopping_list, subtotal) -> List[Tuple[products.Product, int]]:
    """
    Recursive function for order menu.
    Will recursively ask a user to choose a product and an order amount.
    Until the user presses enter to exit the menu twice.
    """

    print("When you want to finish order, enter empty text.\n" "Which product # do you want?")

    product_menu(s)
    # initialize updated inventory
    inventory = s.get_all_available_products()
    product_choice = ask_int_input(0, len(inventory))

    # case: conclude order and exit to main menu
    if (product_choice == 0) or (product_choice == ""):
        return shopping_list, subtotal

    # case: buy a product
    else:
        prod = inventory[product_choice - 1]
        print(f"How many do you want to add to your reservation of: {prod.get_reserved()}.")

        # check if available (for example was a LimitedProduct already reserved beyond max?
        if isinstance(prod.get_available(), int) and prod.get_available() <= 0:
            amount = 0
        else:
            amount = ask_int_input(0, prod.get_available())

        # process new order
        if amount > 0:
            prod.reserve(amount)
            s.add_to_shoppinglist((prod, amount), shopping_list)
            print(
                f"--> Product: {prod.name}. Amount: {amount} added to list! subtotal is {subtotal}"
            )

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
            shopping_list, total = order_menu(s, [], 0)  # generate the shopping list
            total, bill = s.order(shopping_list)
            print(f"\nOrder made! Here's your bill: " f"\n{bill} \n\n")
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
