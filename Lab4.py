"""
------------------------------------------------------------
Application Programming CCGC 5003
Lab 4 - Inventory System (Phase IV)
Summer 2026

Developer Name : Qawiyy Rabiu
Student ID     : N10038749

Description:
This program is Phase-4 of the inventory system. It extends
Phase-3 by adding persistent binary file storage so that
inventory and sales data survive after the application closes
and are automatically reloaded when the application runs again.

Phase-3 features retained:
- Add items to inventory (with unique 5-character serial code)
- Display all items in stock using prettytable
- Search for an item by serial code
- Process a sales transaction
- Display all sales transactions

New features added in Phase-4:
- save_inventory_information(inventory_file, stock)
    Saves the stock nested list to a binary file (inventory.dat)
    using the pickle module. Called after every 'add' operation.

- save_sales_transaction(sales_transaction_file, sales_transaction)
    Saves the sales_transaction dictionary to a binary file
    (sales.dat) using the pickle module. Called after every
    successful 'sales' operation.

- At startup, main() checks if inventory.dat and sales.dat
  exist. If they do, data is loaded back into stock and
  sales_transaction so the application resumes from where
  it left off.

- File size is displayed after every save using os.path.getsize()

Binary files used:
    inventory.dat  — stores stock (list of lists)
    sales.dat      — stores sales_transaction (dictionary)

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
- save_inventory_information(inventory_file, stock)
- save_sales_transaction(sales_transaction_file, sales_transaction)
- main()
------------------------------------------------------------
"""

from prettytable import PrettyTable
from datetime import datetime
import pickle
import os

# --- File name constants ---
INVENTORY_FILE = "inventory.dat"
SALES_FILE = "sales.dat"


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
    Displays the Phase-4 menu options to the user and reads
    their choice (case-insensitive).

    Menu Options:
        add           - to add inventory item
        display       - to display inventory items
        search        - to search an item by item serial code
        sales         - to process sales transaction
        display_sales - to display sales transactions
        end           - to end application

    Parameters: None

    Returns:
        str: The user's menu choice stripped and lowercased.
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

    Returns:
        tuple: (item_name: str, item_price: float,
                item_quantity: int)
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
        a) Must be exactly 5 characters (alphanumeric or
           special characters allowed).
        b) Must not already exist in stock (case-insensitive).

    Parameters:
        item_serial_code (str)  : The serial code to validate.
        stock            (list) : Nested list of all items in
                                  stock. Each inner list is
                                  [name, serial, price, qty].

    Returns:
        bool: True  - serial code is valid and unique.
              False - not 5 characters OR already exists.
    """
    if len(item_serial_code) != 5:
        return False
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
        stock (list): Nested list of all inventory items.
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
        table.add_row([item[0], item[1],
                       f"${item[2]:.2f}", item[3]])
    print(table)


# ----------------------------------------------------
# Function Name: search
# ----------------------------------------------------
def search(stock):
    """
    Searches for an item in the stock by its serial code.

    Conditions handled:
        - Empty stock: displays a message and returns.
        - Invalid serial code (not 5 chars): informs user.
        - Item found: displays in PrettyTable format.
        - Item not found: displays not-found message.

    Parameters:
        stock (list): Nested list of all inventory items.
                      Each inner list: [name, serial, price, qty]

    Returns: None
    """
    if not stock:
        print(" Stock has no items - empty stock ....  Cannot search an empty stock")
        return

    search_code = input(
        " Please enter the Item Serial Code to search an item:  "
    ).strip()

    if len(search_code) != 5:
        print(" Invalid serial code - must be exactly 5 characters")
        return

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
        table.add_row([found_item[0], found_item[1],
                       f"${found_item[2]:.2f}", found_item[3]])
        print(table)
    else:
        print(" Item is not available in stock")


# ----------------------------------------------------
# Function Name: sales_transactions
# ----------------------------------------------------
def sales_transactions(stock, sales_transaction):
    """
    Processes a sales transaction from the inventory.

    Checks all conditions before processing:
        Condition 1 - Stock must not be empty.
        Condition 2 - Serial code must exist in stock.
        Condition 3 - Quantity requested must not exceed
                      available stock quantity.

    If all conditions pass:
        - Date and time recorded using datetime.now().
        - Transaction saved in sales_transaction dictionary:
            Key   = item_serial_code (str)
            Value = [date_time, item_name, serial_code,
                     item_price, qty_sold]
        - Stock quantity reduced by qty_to_buy.
        - If quantity reaches 0, item removed from stock.

    Parameters:
        stock             (list) : Nested list of inventory items.
                                   Each inner list:
                                   [name, serial, price, qty]
        sales_transaction (dict) : Dictionary storing all sales.
                                   Key   = item_serial_code (str)
                                   Value = [date_time, name,
                                            serial, price, qty]

    Returns:
        None  (stock and sales_transaction modified in place)
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

    # Get quantity — validate: must be a positive whole number
    while True:
        qty_input = input(" Enter quantity to purchase:  ").strip()
        if qty_input.isdigit() and int(qty_input) > 0:
            qty_to_buy = int(qty_input)
            break
        else:
            print(" Invalid quantity. Please enter a positive whole number.")

    # Condition 2: Check if serial code exists in stock
    found_item = None
    found_index = None
    for i, item in enumerate(stock):
        if item[1].lower() == serial_code.lower():
            found_item = item
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

    # Record current date and time
    transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Save transaction in dictionary — key is the serial code
    sales_transaction[serial_code] = [
        transaction_time,
        found_item[0],
        found_item[1],
        found_item[2],
        qty_to_buy
    ]

    # Reduce stock quantity
    stock[found_index][3] -= qty_to_buy

    # Remove item from stock entirely if all units sold
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

    If no sales have been made yet, a message is shown.

    Table Columns:
        Transaction date-time | Item Name | Item Serial Code
        | Item Price | Item Quantity

    Item price is displayed with '$' and two decimal places.

    Parameters:
        sales_transaction (dict): Dictionary of all sales.
                                  Key   = item_serial_code (str)
                                  Value = [date_time, name,
                                           serial, price, qty]

    Returns: None
    """
    display_header()
    print()
    print("#" * 100)

    if not sales_transaction:
        print(" No sales transactions completed so far .. .. .")
        print(" There have been no sales transactions yet!")
        return

    table = PrettyTable()
    table.field_names = [
        "Transaction date-time", "Item Name",
        "Item Serial Code", "Item Price", "Item Quantity"
    ]

    for key, record in sales_transaction.items():
        table.add_row([
            record[0],
            record[1],
            record[2],
            f"${record[3]:.2f}",
            record[4]
        ])

    print(table)


# ----------------------------------------------------
# Function Name: save_inventory_information
# ----------------------------------------------------
def save_inventory_information(inventory_file, stock):
    """
    Saves the stock (nested list of inventory items) to a
    binary file using the pickle module.

    The file is opened in write-binary mode ('wb'), which
    overwrites any previous contents so the file always
    reflects the current state of the stock.

    After saving, the file size is displayed using
    os.path.getsize() to confirm data was written.

    This function is called:
        - After every successful 'add' operation in main()
        - After every successful 'sales' operation in main()

    Parameters:
        inventory_file (str)  : The filename for the inventory
                                binary file (e.g. 'inventory.dat')
        stock          (list) : Nested list of all inventory items.
                                Each inner list:
                                [name, serial, price, qty]

    Returns: None
    """
    # Open in write-binary ('wb') mode to overwrite with current stock
    with open(inventory_file, 'wb') as file:
        pickle.dump(stock, file)

    # Show the updated file size after saving
    file_size = os.path.getsize(inventory_file)
    print(f" inventory.dat saved  —  file size: {file_size} bytes")


# ----------------------------------------------------
# Function Name: save_sales_transaction
# ----------------------------------------------------
def save_sales_transaction(sales_transaction_file, sales_transaction):
    """
    Saves the sales_transaction dictionary to a binary file
    using the pickle module.

    The file is opened in write-binary mode ('wb'), which
    overwrites any previous contents so the file always
    reflects the current state of all sales transactions.

    After saving, the file size is displayed using
    os.path.getsize() to confirm data was written.

    This function is called:
        - After every successful 'sales' operation in main()

    Parameters:
        sales_transaction_file (str)  : The filename for the
                                        sales binary file
                                        (e.g. 'sales.dat')
        sales_transaction      (dict) : Dictionary of all sales.
                                        Key   = serial_code (str)
                                        Value = [date_time, name,
                                                 serial, price, qty]

    Returns: None
    """
    # Open in write-binary ('wb') mode to overwrite with current sales
    with open(sales_transaction_file, 'wb') as file:
        pickle.dump(sales_transaction, file)

    # Show the updated file size after saving
    file_size = os.path.getsize(sales_transaction_file)
    print(f" sales.dat saved  —  file size: {file_size} bytes")


# ----------------------------------------------------
# Function Name: main
# ----------------------------------------------------
def main():
    """
    Main application function. Runs the Phase-4 menu-driven
    inventory system in a loop until the user chooses to end.

    Phase-4 Updates to main():
        - On startup, checks if inventory.dat and sales.dat
          exist using os.path.exists().
        - If inventory.dat exists, loads stock data from it
          using pickle (read-binary mode 'rb').
        - If sales.dat exists, loads sales_transaction data
          from it using pickle (read-binary mode 'rb').
        - After every 'add' operation, calls:
              save_inventory_information() to update inventory.dat
        - After every successful 'sales' operation, calls:
              save_inventory_information() to update inventory.dat
              save_sales_transaction() to update sales.dat
        - All Phase-3 options and logic retained unchanged.

    Data Structures:
        stock (list of lists):
            Each inner list: [name (str), serial (str),
                              price (float), qty (int)]

        sales_transaction (dict):
            Key   = item_serial_code (str)
            Value = [date_time (str), name (str), serial (str),
                     price (float), qty_sold (int)]

    Binary Files:
        inventory.dat  — persists stock between runs
        sales.dat      — persists sales_transaction between runs

    Parameters: None

    Returns: None
    """
    # Initialise empty data structures
    stock = []
    sales_transaction = {}

    # --- Load existing data from binary files if they exist ---

    # Load inventory stock from file (read-binary 'rb' mode)
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'rb') as file:
            stock = pickle.load(file)
        print(f" Inventory data loaded from {INVENTORY_FILE}  "
              f"—  file size: {os.path.getsize(INVENTORY_FILE)} bytes")

    # Load sales transactions from file (read-binary 'rb' mode)
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'rb') as file:
            sales_transaction = pickle.load(file)
        print(f" Sales data loaded from {SALES_FILE}  "
              f"—  file size: {os.path.getsize(SALES_FILE)} bytes")

    # Display header on startup
    display_header()

    # Main application loop
    while True:

        choice = menu()

        if choice == "add":
            # Read item name, price, quantity
            item_name, item_price, item_quantity = read_item()

            # Keep asking for serial code until a valid unique one entered
            while True:
                item_serial_code = input(
                    " Enter 5-character item serial code"
                    " - for the item to be added to the stock:  "
                ).strip()
                if is_unique(item_serial_code, stock):
                    break
                else:
                    print(" Serial code invalid or already exists. Try again.")

            # Save item as a list and append to stock
            item = [item_name, item_serial_code, item_price, item_quantity]
            stock.append(item)

            # Save updated stock to inventory.dat immediately after add
            save_inventory_information(INVENTORY_FILE, stock)

        elif choice == "display":
            display_stock(stock)

        elif choice == "search":
            search(stock)

        elif choice == "sales":
            # Record stock length before to detect if sale was successful
            stock_len_before = len(stock)
            sales_len_before = len(sales_transaction)

            sales_transactions(stock, sales_transaction)

            # Save both files if the sale changed the data
            if (len(stock) != stock_len_before or
                    len(sales_transaction) != sales_len_before):
                save_inventory_information(INVENTORY_FILE, stock)
                save_sales_transaction(SALES_FILE, sales_transaction)

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