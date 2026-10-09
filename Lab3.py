"""
------------------------------------------------------------
Application Programming CCGC 5003
Lab 3 - Inventory System (Phase III)
Summer 2026

Developer Name : Qawiyy Rabiu
Student ID     : N10038749

Description:
This program is Phase-3 of the inventory system. It extends
Phase-2 by introducing sales transactions stored in a
Python Dictionary.

Phase-2 features retained:
- Add items to inventory (with unique 5-character serial code)
- Display all items in stock using prettytable
- Search for an item by serial code

New features added in Phase-3:
- Process a sales transaction (sales option)
- Display all sales transactions (display_sales option)
- Sales records stored in a Dictionary where:
    key   = item_serial_code (str)
    value = [transaction_date_time, item_name,
             item_serial_code, item_price, qty_sold]
- Stock quantity reduced after each sale
- Item row removed from stock entirely when qty reaches 0
- Date and time recorded using Python datetime module

The application uses the following functions:
- display_developer_info()
- display_header()
- menu()
- read_item()
- is_unique(item_serial_code, stock)
- display_stock(stock)
- search(stock)
- sales_transactions(stock, sales_transaction)
- display_sales_transactions(sales_transaction)
- main()
------------------------------------------------------------
"""

from prettytable import PrettyTable
from datetime import datetime


# ----------------------------------------------------
# Function Name: display_developer_info
# ----------------------------------------------------
def display_developer_info():
    """
    Displays the developer's name and student ID
    right-aligned on the terminal, with colons aligned.

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
    Displays the updated Phase-3 menu options to the user
    and reads their choice (case-insensitive).

    Menu Options:
        add           - to add inventory item
        display       - to display inventory items
        search        - to search an item by item serial code
        sales         - to process sales transaction
        display_sales - to display sales transactions
        end           - to end application

    Parameters: None

    Returns: str: The user's menu choice stripped and lowercased.
    """
    print()
    print(f"    {'add:':<16}to add inventory item")
    print(f"    {'display:':<16}to display inventory items")
    print(f"    {'search:':<16}to search an item by item serial code")
    print(f"    {'sales:':<16}to process sales transaction")
    print(f"    {'display_sales:':<16}to display sales transactions")
    print(f"    {'end:':<16}to end application")
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
    The serial code is NOT read here — it is handled
    separately in main() via is_unique().

    Parameters: None

    Returns: tuple: (item_name: str, item_price: float,
                item_quantity: int)
    """
    display_header()
    print()
    item_name     = input(" Enter item name - for item to be added to the stock:  ")
    item_price    = float(input(" Enter price of the item:   $ ").replace(",", ""))
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
              False - if not 5 characters OR already exists.
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
    Displays all items currently in the stock in a formatted
    table using the PrettyTable module.

    If the stock is empty, an appropriate message is shown
    instead of an empty table.

    Table Columns:
        Item Name | Item Serial Code | Item Price | Item Quantity

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
    table.field_names = ["Item Name", "Item Serial Code",
                         "Item Price", "Item Quantity"]
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
    code, the user is informed.
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

    search_code = input(
        " Please enter the Item Serial Code to search an item:  "
    ).strip()

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
        table.field_names = ["Item Name", "Item Serial Code",
                             "Item Price", "Item Quantity"]
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
# Function Name: sales_transactions
# ----------------------------------------------------
def sales_transactions(stock, sales_transaction):
    """
    Processes a sales transaction from the inventory.

    This function checks all possible conditions before
    processing the sale:
        Condition 1 - Stock must not be empty.
        Condition 2 - Serial code entered must exist in stock.
        Condition 3 - Quantity requested must not exceed
                      available stock quantity.

    If all conditions pass, the sale is processed:
        - Current date and time recorded using datetime.now().
        - Transaction saved in the sales_transaction dictionary:
            Key   = item_serial_code (str)
            Value = [date_time, item_name, serial_code,
                     item_price, qty_sold]
        - Stock quantity reduced by qty_to_buy.
        - If remaining quantity reaches 0, the item row is
          completely removed from the stock list using pop().

    Parameters:
        stock             (list) : Nested list of inventory items.
                                   Each inner list:
                                   [name, serial, price, qty]
        sales_transaction (dict) : Dictionary storing all sales.
                                   Key   = item_serial_code (str)
                                   Value = [date_time, name,
                                            serial, price, qty]

    Returns: None  (stock and sales_transaction modified in place)
    """
    display_header()
    print()
    print("#" * 100)

    # Condition 1: Cannot sell if stock is empty
    if not stock:
        print(" Stock is empty - there are no items to sell")
        return

    # Get the serial code of the item to purchase
    serial_code = input(
        " Enter the item serial code of the item to purchase:  "
    ).strip()

    # Get quantity to buy — keep asking until a valid positive integer entered
    while True:
        qty_input = input(" Enter quantity to purchase:  ").strip()
        if qty_input.isdigit() and int(qty_input) > 0:
            qty_to_buy = int(qty_input)
            break
        else:
            print(" Invalid quantity. Please enter a positive whole number.")

    # Condition 2: Check if serial code exists in stock
    found_item  = None
    found_index = None
    for i, item in enumerate(stock):
        if item[1].lower() == serial_code.lower():
            found_item  = item
            found_index = i
            break

    if found_item is None:
        print(f" The item with item_serial_code, {serial_code} is not in stock")
        return

    # Condition 3: Check if enough quantity is available
    if qty_to_buy > found_item[3]:
        print(" Not enough quantity in stock, "
              "sales will not go through - please try later")
        return

    # --- All conditions passed: process the sale ---

    # Record current date and time of this transaction
    transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Save transaction in dictionary — key is the serial code
    sales_transaction[serial_code] = [
        transaction_time,   # element 0: date and time
        found_item[0],      # element 1: item name
        found_item[1],      # element 2: item serial code
        found_item[2],      # element 3: item price
        qty_to_buy          # element 4: quantity sold
    ]

    # Update stock: reduce quantity by amount sold
    stock[found_index][3] -= qty_to_buy

    # If all units of this item were sold, remove it from stock entirely
    if stock[found_index][3] == 0:
        stock.pop(found_index)

    print("=" * 100)


# ----------------------------------------------------
# Function Name: display_sales_transactions
# ----------------------------------------------------
def display_sales_transactions(sales_transaction):
    """
    Displays all recorded sales transactions in a formatted
    table using the PrettyTable module.

    Conditions handled:
        - If no sales have been made yet, two messages are
          displayed instead of an empty table.

    Table Columns:
        Transaction date-time | Item Name | Item Serial Code
        | Item Price | Item Quantity

    Each row is retrieved from the sales_transaction dictionary.
    Item price is displayed with '$' and two decimal places.
    The complete table with heading and all rows is printed.

    Parameters:
        sales_transaction (dict): Dictionary of all sales records.
                                  Key   = item_serial_code (str)
                                  Value = [date_time, name,
                                           serial, price, qty]

    Returns: None
    """
    display_header()
    print()
    print("#" * 100)

    # Condition: No sales transactions made yet
    if not sales_transaction:
        print(" No sales transactions completed so far .. .. .")
        print(" There have been no sales transactions yet!")
        return

    # Create table heading
    table = PrettyTable()
    table.field_names = [
        "Transaction date-time",
        "Item Name",
        "Item Serial Code",
        "Item Price",
        "Item Quantity"
    ]

    # Retrieve each record from the dictionary and render as a table row
    for key, record in sales_transaction.items():
        table.add_row([
            record[0],             # Transaction date-time
            record[1],             # Item Name
            record[2],             # Item Serial Code
            f"${record[3]:.2f}",  # Item Price with $ and 2 decimal places
            record[4]              # Item Quantity sold
        ])

    # Display complete table with heading and all rows
    print(table)


# ----------------------------------------------------
# Function Name: main
# ----------------------------------------------------
def main():
    """
    Main application function. Runs the updated Phase-3
    menu-driven inventory system in a loop until the user
    chooses to end.

    Phase-3 Updates to main():
        - sales_transaction dictionary initialised as {}.
        - Two new menu options added and handled:
            'sales'         -> calls sales_transactions()
            'display_sales' -> calls display_sales_transactions()
        - Invalid choice message updated with new options.
        - All Phase-2 options and logic retained unchanged.

    Program Flow:
        1. Display header on startup.
        2. Show menu and read user's choice.
        3. Route to the correct function based on choice.
        4. Repeat until 'end' is chosen.

    Data Structures:
        stock (list of lists):
            Each inner list: [name (str), serial (str),
                              price (float), qty (int)]

        sales_transaction (dict):
            Key   = item_serial_code (str)
            Value = [date_time (str), name (str), serial (str),
                     price (float), qty_sold (int)]

    Parameters: None

    Returns: None
    """
    # Initialise empty stock list (nested list of items)
    stock = []

    # Initialise empty sales transaction dictionary
    sales_transaction = {}

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
                    continue

            # Save item in a list and append to stock
            item = [item_name, item_serial_code, item_price, item_quantity]
            stock.append(item)

        elif choice == "display":
            display_stock(stock)

        elif choice == "search":
            search(stock)

        elif choice == "sales":
            sales_transactions(stock, sales_transaction)

        elif choice == "display_sales":
            display_sales_transactions(sales_transaction)

        elif choice == "end":
            print(" Thank you - Ending application now .. .. ..")
            break

        else:
            print(" Enter valid choice .. ... from the options "
                  "'[add, display, search, sales, display_sales, end ]'")


# -------- MAIN APPLICATION --------
if __name__ == "__main__":
    main()