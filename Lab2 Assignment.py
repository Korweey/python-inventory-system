"""
------------------------------------------------------------
Application Programming CCGC 5003
Lab 2 - Inventory System (Phase II)
Summer 2026

Developer Name : Qawiyy Rabiu
Student ID     : N10038749

Description:
This program is Phase-2 of the inventory system. It extends
Phase-1 by introducing a menu-driven interface and storing
multiple inventory items using a nested List (stock).

Features:
- Add items to inventory (with unique 5-character serial code)
- Display all items in stock using prettytable
- Search for an item by serial code
- End the application gracefully

The application uses the following functions:
- display_developer_info()
- display_header()
- menu()
- read_item()
- is_unique(item_serial_code, stock)
- display_stock(stock)
- search(stock)
- main()
------------------------------------------------------------
"""

from prettytable import PrettyTable

# ----------------------------------------------------
# Function Name: display_developer_info
# ----------------------------------------------------
def display_developer_info():
    """
    Displays the developer's name and student ID
    right-aligned on the terminal.

    Parameters: None

    Returns: None
    """
    print(f"{'Name:':>12}    {'Qawiyy Rabiu'}".rjust(80))
    print(f"{'Student ID:':>12}    {'N10038749'}".rjust(77))

# ----------------------------------------------------
# Function Name: display_header
# ----------------------------------------------------
def display_header():
    """
    Displays the application header including the developer
    info, a separator line, and the company name centred.

    Parameters: None

    Returns: None
    """
    display_developer_info()
    print("=" * 80)
    print(f"{'Quality Items & Services':^78}")
    print(f"{'----------------------------------------':^78}")

# ----------------------------------------------------
# Function Name: menu
# ----------------------------------------------------
def menu():
    """
    Displays the main menu options to the user and reads
    their choice (case-insensitive).

    Menu Options:
        add      - to add inventory item
        display  - to display inventory items
        search   - to search an item by item serial code
        end      - to end application

    Parameters: None

    Returns:
        str: The user's menu choice in lowercase.
    """
    print()
    print(f"    {'add:':<12}to add inventory item")
    print(f"    {'display:':<12}to display inventory items")
    print(f"    {'search:':<12}to search an item by item serial code")
    print(f"    {'end:':<12}to end application")
    print()
    choice = input(" Please enter your choice from the options:  ")
    return choice.strip().lower()

# ----------------------------------------------------
# Function Name: read_item
# ----------------------------------------------------
def read_item():
    """
    Prompts the user to enter item information:
    item name, item price, and item quantity.
    The serial code is NOT read here — it is handled separately in main() via is_unique().

    Parameters: None

    Returns:
        tuple: (item_name: str, item_price: float, item_quantity: int)
    """
    display_header()
    print()
    item_name = input(" Enter item name - for item to be added to the stock:  ")
    item_price = float(input(" Enter price of the item:   $ ").replace(",", ""))
    item_quantity = int(input(" Enter the quantity of the items to be stocked:  "))
    return item_name, item_price, item_quantity

# ----------------------------------------------------
# Function Name: is_unique
# ----------------------------------------------------
def is_unique(item_serial_code, stock):
    """
    Validates that the given item_serial_code is exactly
    5 characters long and does not already exist in stock.

    Validation Rules:
        a) The serial code must be exactly 5 characters
           (alphanumeric or special characters allowed).
        b) The serial code must not already exist in stock.

    Parameters:
        item_serial_code (str)  : The serial code to validate.
        stock            (list) : The nested list of all items
                                  currently in stock. Each inner
                                  list is [name, serial, price, qty].

    Returns:
        bool: True  - if the serial code is valid and unique.
              False - if it is not 5 characters OR already exists.
    """
    # Check length is exactly 5 characters
    if len(item_serial_code) != 5:
        return False

    # Check uniqueness against all items already in stock
    for item in stock:
        if item[1].lower() == item_serial_code.lower():
            return False

    return True

# ----------------------------------------------------
# Function Name: display_stock
# ----------------------------------------------------
def display_stock(stock):
    """
    Displays all items currently in the stock in a formatted table using the PrettyTable module.

    If the stock is empty, an appropriate message is shown instead of an empty table.

    Table Columns: Item Name | Item Serial Code | Item Price | Item Quantity

    Parameters:
        stock (list): The nested list of all inventory items.
                      Each inner list: [name, serial, price, qty]

    Returns: None
    """
    display_header()
    print()

    if not stock:
        print(" At this time, stock is empty .. .. ..")
        return

    table = PrettyTable()
    table.field_names = ["Item Name", "Item Serial Code", "Item Price", "Item Quantity"]

    for item in stock:
        table.add_row([
            item[0],
            item[1],
            f"${item[2]:.2f}",
            item[3]
        ])

    print(table)


# ----------------------------------------------------
# Function Name: search
# ----------------------------------------------------
def search(stock):
    """
    Searches for an item in the stock by its serial code.

    If the stock is empty, an appropriate message is shown.
    If the serial code entered is not a valid 5-character
    alphanumeric code, the user is informed.
    If the item is found, it is displayed in table format
    using PrettyTable. If not found, a not-found message
    is displayed.

    Parameters:
        stock (list): The nested list of all inventory items.
                      Each inner list: [name, serial, price, qty]

    Returns: None
    """
    # Cannot search if stock is empty
    if not stock:
        print(" Stock has no items - empty stock ....  Cannot search an empty stock")
        return

    search_code = input(" Please enter the Item Serial Code to search an item:  ").strip()

    # Validate the serial code entered for searching
    if len(search_code) != 5:
        print(" Invalid serial code - must be exactly 5 characters")
        return

    # Search through the stock
    found_item = None
    for item in stock:
        if item[1].lower() == search_code.lower():
            found_item = item
            break

    if found_item:
        display_header()
        print()
        table = PrettyTable()
        table.field_names = ["Item Name", "Item Serial Code", "Item Price", "Item Quantity"]
        table.add_row([
            found_item[0],
            found_item[1],
            f"${found_item[2]:.2f}",
            found_item[3]
        ])
        print(table)
    else:
        print(" Item is not available in stock")


# ----------------------------------------------------
# Function Name: main
# ----------------------------------------------------
def main():
    """
    Main application function. Runs the menu-driven inventory
    system in a loop until the user chooses to end.

    Program Flow:
        1. Display developer information and header.
        2. Display the menu and read the user's choice.
        3. Based on the choice:
           - 'add'     : Read item info, validate and ensure a
                         unique 5-character serial code, then
                         save the item as a list appended to stock.
           - 'display' : Display all items in stock via prettytable.
           - 'search'  : Search for an item by serial code.
           - 'end'     : Print farewell message and exit the loop.
           - other     : Display an invalid-choice message.
        4. Repeat until 'end' is chosen.

    Data Structure:
        stock (list of lists): Each inner list holds one item:
            [item_name (str), item_serial_code (str),
             item_price (float), item_quantity (int)]

    Parameters: None

    Returns: None
    """
    # Initialize empty stock (nested list)
    stock = []

    # Display header on startup
    display_header()

    # Main application loop
    while True:

        choice = menu()

        if choice == "add":
            # Read item name, price, quantity
            item_name, item_price, item_quantity = read_item()

            # Keep asking for serial code until a valid unique one is entered
            while True:
                item_serial_code = input(
                    " Enter 5-character item serial code"
                    " - for the item to be added to the stock:  "
                ).strip()

                if is_unique(item_serial_code, stock):
                    break
                else:
                    # Re-prompt without re-reading other fields
                    continue

            # Save item in a list and append to stock
            item = [item_name, item_serial_code, item_price, item_quantity]
            stock.append(item)

        elif choice == "display":
            display_stock(stock)

        elif choice == "search":
            search(stock)

        elif choice == "end":
            print(" Thank you - Ending application now .. .. ..")
            break

        else:
            print(f" Enter valid choice .. ... from the options '[add, display, search, end ]'")


# -------- MAIN APPLICATION --------
if __name__ == "__main__":
    main()