"""
------------------------------------------------------------
Application Programming CCGC 5003
Lab 5 - Inventory System (Phase V)
Summer 2026

Developer Name : Qawiyy Rabiu
Student ID     : N10038749

Description:
This program is Phase-5 of the inventory system. It extends
Phase-4 by adding encryption to the binary file storage.
All inventory and sales data is now encrypted before being
saved to disk, and decrypted when loaded back.

Phase-4 features retained:
- Add items to inventory (with unique 5-character serial code)
- Display all items in stock using prettytable
- Search for an item by serial code
- Process a sales transaction
- Display all sales transactions
- Persistent binary file storage

New features added in Phase-5:
- Encryption key managed in key_file.dat using Fernet
- encrypt_and_save_stock(key, stock, enc_stock_file)
- encrypt_and_save_sales_transaction(key, sales_transaction,
                                     enc_sales_file)
- decrypt_and_return_stock(key, enc_stock_file)
- decrypt_and_return_sales_transactions(key, enc_sales_file)

Binary Files used:
    key_file.dat             — stores the Fernet encryption key
    encrypted_stock_file.dat — stores encrypted inventory stock
    encrypted_sales_file.dat — stores encrypted sales transactions

On startup:
    - key_file.dat is checked. If it exists and has data,
      the key is read. If empty or missing, a new key is
      generated and saved.
    - If encrypted_stock_file.dat has data, stock is
      decrypted and loaded.
    - If encrypted_sales_file.dat has data, sales_transaction
      is decrypted and loaded.

File sizes are displayed after every save operation.
------------------------------------------------------------
"""

from prettytable import PrettyTable
from datetime import datetime
from cryptography.fernet import Fernet
import pickle
import os


# --- File name constants ---
KEY_FILE       = "key_file.dat"
ENC_STOCK_FILE = "encrypted_stock_file.dat"
ENC_SALES_FILE = "encrypted_sales_file.dat"


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
    Displays the Phase-5 menu options to the user and reads
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
    The serial code is handled separately in main()
    via is_unique().

    Parameters: None

    Returns:
        tuple: (item_name: str, item_price: float,
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
    After displaying, shows the size of the encrypted stock
    file if it exists.

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

    # Show encrypted file size after displaying stock
    if os.path.exists(ENC_STOCK_FILE):
        size = os.path.getsize(ENC_STOCK_FILE)
        print(f" The size of inventory/stock encrypted file is:  {size} bytes")


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
        - Transaction saved in sales_transaction dictionary.
        - Stock quantity reduced by qty_to_buy.
        - If quantity reaches 0, item removed from stock.

    Parameters:
        stock             (list) : Nested list of inventory.
                                   Each inner list:
                                   [name, serial, price, qty]
        sales_transaction (dict) : Dictionary of all sales.
                                   Key   = serial_code (str)
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

    serial_code = input(
        " Enter the item serial code of the item to purchase:  "
    ).strip()

    # Validate quantity input
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

    # Record date and time
    transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Save transaction in dictionary
    sales_transaction[serial_code] = [
        transaction_time,
        found_item[0],
        found_item[1],
        found_item[2],
        qty_to_buy
    ]

    # Reduce stock quantity
    stock[found_index][3] -= qty_to_buy

    # Remove item from stock if all units sold
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
    After displaying, shows the size of the encrypted sales
    file if it exists.

    Table Columns:
        Transaction date-time | Item Name | Item Serial Code
        | Item Price | Item Quantity

    Parameters:
        sales_transaction (dict): Dictionary of all sales.
                                  Key   = serial_code (str)
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

    # Show encrypted file size after displaying sales
    if os.path.exists(ENC_SALES_FILE):
        size = os.path.getsize(ENC_SALES_FILE)
        print(f" The size of sales transaction encrypted file is:  {size} bytes")


# ----------------------------------------------------
# Function Name: encrypt_and_save_stock
# ----------------------------------------------------
def encrypt_and_save_stock(key, stock, enc_stock_file):
    """
    Encrypts the stock (nested list) and saves it to a
    binary file using Fernet symmetric encryption.

    Process:
        1. Convert stock to bytes using pickle.dumps() —
           this serializes the Python list into byte format.
        2. Create a Fernet cipher object using the key.
        3. Encrypt the byte data using cipher.encrypt().
        4. Open the encrypted stock file in write-binary
           ('wb') mode and write the encrypted bytes.
        5. Display the file size after saving.

    This function is called after every successful 'add'
    operation and after every successful 'sales' operation
    in main().

    Parameters:
        key            (bytes) : The Fernet encryption key.
        stock          (list)  : Nested list of inventory items.
                                 Each inner list:
                                 [name, serial, price, qty]
        enc_stock_file (str)   : Filename of the encrypted
                                 stock binary file.
                                 (encrypted_stock_file.dat)

    Returns: None
    """
    # Convert stock list to bytes (byte formation from data type)
    stock_bytes = pickle.dumps(stock)

    # Create Fernet cipher and encrypt the byte data
    cipher          = Fernet(key)
    encrypted_bytes = cipher.encrypt(stock_bytes)

    # Save encrypted contents to binary file in write-binary mode
    with open(enc_stock_file, 'wb') as file:
        file.write(encrypted_bytes)

    # Display file size after saving
    file_size = os.path.getsize(enc_stock_file)
    print(f" encrypted_stock_file.dat saved  —  file size: {file_size} bytes")


# ----------------------------------------------------
# Function Name: encrypt_and_save_sales_transaction
# ----------------------------------------------------
def encrypt_and_save_sales_transaction(key, sales_transaction,
                                       enc_sales_file):
    """
    Encrypts the sales_transaction dictionary and saves it
    to a binary file using Fernet symmetric encryption.

    Process:
        1. Check if sales_transaction has data before saving.
        2. Convert sales_transaction dict to bytes using
           pickle.dumps() — byte format conversion.
        3. Create a Fernet cipher object using the key.
        4. Encrypt the byte data using cipher.encrypt().
        5. Open the encrypted sales file in write-binary
           ('wb') mode and write the encrypted bytes.
        6. Display the file size after saving.

    This function is called after every successful 'sales'
    operation in main().

    Parameters:
        key               (bytes) : The Fernet encryption key.
        sales_transaction (dict)  : Dictionary of all sales.
                                    Key   = serial_code (str)
                                    Value = [date_time, name,
                                             serial, price, qty]
        enc_sales_file    (str)   : Filename of the encrypted
                                    sales binary file.
                                    (encrypted_sales_file.dat)

    Returns: None
    """
    # Check data contents — only save if there are sales records
    if not sales_transaction:
        return

    # Convert sales dictionary to bytes (byte format conversion)
    sales_bytes = pickle.dumps(sales_transaction)

    # Create Fernet cipher and encrypt the byte data
    cipher          = Fernet(key)
    encrypted_bytes = cipher.encrypt(sales_bytes)

    # Save encrypted contents to binary file in write-binary mode
    with open(enc_sales_file, 'wb') as file:
        file.write(encrypted_bytes)

    # Display file size after saving
    file_size = os.path.getsize(enc_sales_file)
    print(f" encrypted_sales_file.dat saved  —  file size: {file_size} bytes")


# ----------------------------------------------------
# Function Name: decrypt_and_return_stock
# ----------------------------------------------------
def decrypt_and_return_stock(key, enc_stock_file):
    """
    Reads the encrypted stock file, decrypts its contents,
    converts it back to the proper Python data type (nested
    list), and returns it to the calling function.

    Process:
        1. Open the encrypted stock file in read-binary
           ('rb') mode and read the encrypted bytes.
        2. Create a Fernet cipher object using the key.
        3. Decrypt the bytes using cipher.decrypt().
        4. Convert decrypted bytes back to Python list using
           pickle.loads() — restores the proper data type.
        5. Return the decrypted stock list.

    This function is called in main() at startup if
    encrypted_stock_file.dat exists and has data.

    Parameters:
        key            (bytes) : The Fernet encryption key.
        enc_stock_file (str)   : Filename of the encrypted
                                 stock binary file.
                                 (encrypted_stock_file.dat)

    Returns:
        list: The decrypted stock (nested list of inventory
              items). Each inner list: [name, serial, price, qty]
    """
    # Open encrypted file in read-binary mode and read bytes
    with open(enc_stock_file, 'rb') as file:
        encrypted_bytes = file.read()

    # Decrypt using Fernet cipher — converts back to original bytes
    cipher          = Fernet(key)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # Convert decrypted bytes back to proper Python list data type
    stock = pickle.loads(decrypted_bytes)

    # Return the decrypted stock data to the calling function
    return stock


# ----------------------------------------------------
# Function Name: decrypt_and_return_sales_transactions
# ----------------------------------------------------
def decrypt_and_return_sales_transactions(key, enc_sales_file):
    """
    Reads the encrypted sales file, decrypts its contents,
    converts it back to the proper Python data type
    (dictionary), and returns it to the calling function.

    Process:
        1. Open the encrypted sales file in read-binary
           ('rb') mode and read the encrypted bytes.
        2. Create a Fernet cipher object using the key.
        3. Decrypt the bytes using cipher.decrypt().
        4. Convert decrypted bytes back to Python dictionary
           using pickle.loads() — restores the proper data type.
        5. Return the decrypted sales_transaction dictionary.

    This function is called in main() at startup if
    encrypted_sales_file.dat exists and has data.

    Parameters:
        key            (bytes) : The Fernet encryption key.
        enc_sales_file (str)   : Filename of the encrypted
                                 sales binary file.
                                 (encrypted_sales_file.dat)

    Returns:
        dict: The decrypted sales_transaction dictionary.
              Key   = item_serial_code (str)
              Value = [date_time, name, serial, price, qty]
    """
    # Open encrypted file in read-binary mode and read bytes
    with open(enc_sales_file, 'rb') as file:
        encrypted_bytes = file.read()

    # Decrypt using Fernet cipher
    cipher          = Fernet(key)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # Convert decrypted bytes back to proper Python dict data type
    sales_transaction = pickle.loads(decrypted_bytes)

    # Return the decrypted sales transaction data to calling function
    return sales_transaction


# ----------------------------------------------------
# Function Name: main
# ----------------------------------------------------
def main():
    """
    Main application function. Runs the Phase-5 menu-driven
    inventory system in a loop until the user chooses to end.

    Phase-5 Updates to main():
        Key Management:
            - Checks if key_file.dat exists and has data.
            - If yes: reads the existing encryption key from
              the file in read-binary ('rb') mode.
            - If file is empty or missing: generates a new
              Fernet key, creates key_file.dat, and saves
              the key in write-binary ('wb') mode.
              Also creates empty encrypted_stock_file.dat
              and encrypted_sales_file.dat.

        Loading encrypted data on startup:
            - If encrypted_stock_file.dat has data: calls
              decrypt_and_return_stock() to load stock.
            - If encrypted_sales_file.dat has data: calls
              decrypt_and_return_sales_transactions() to
              load sales_transaction.

        Saving encrypted data after changes:
            - After every 'add': calls
              encrypt_and_save_stock()
            - After every successful 'sales': calls
              encrypt_and_save_stock() and
              encrypt_and_save_sales_transaction()

        File size is displayed after every save via the
        save functions themselves.

    Data Structures:
        stock (list of lists):
            Each inner list: [name (str), serial (str),
                              price (float), qty (int)]
        sales_transaction (dict):
            Key   = item_serial_code (str)
            Value = [date_time (str), name (str),
                     serial (str), price (float),
                     qty_sold (int)]

    Parameters: None

    Returns: None
    """
    # Initialise empty data structures
    stock             = []
    sales_transaction = {}

    # --- Key Management ---
    # Check if key_file.dat exists and has data
    if os.path.exists(KEY_FILE) and os.path.getsize(KEY_FILE) > 0:
        # Read existing key from file in read-binary mode
        with open(KEY_FILE, 'rb') as kf:
            key = kf.read()
        print(f" Encryption key loaded from {KEY_FILE}")
    else:
        # Generate a new Fernet encryption key
        key = Fernet.generate_key()

        # Save new key to key_file.dat in write-binary mode
        with open(KEY_FILE, 'wb') as kf:
            kf.write(key)
        print(f" New encryption key generated and saved to {KEY_FILE}")

        # Create empty encrypted stock and sales files
        with open(ENC_STOCK_FILE, 'wb') as f:
            pass
        with open(ENC_SALES_FILE, 'wb') as f:
            pass
        print(f" Created empty {ENC_STOCK_FILE} and {ENC_SALES_FILE}")

    # --- Load encrypted data from files if they have content ---

    # Load stock from encrypted_stock_file.dat if it has data
    if os.path.exists(ENC_STOCK_FILE) and os.path.getsize(ENC_STOCK_FILE) > 0:
        stock = decrypt_and_return_stock(key, ENC_STOCK_FILE)
        size  = os.path.getsize(ENC_STOCK_FILE)
        print(f" Stock loaded from {ENC_STOCK_FILE}  —  file size: {size} bytes")

    # Load sales from encrypted_sales_file.dat if it has data
    if os.path.exists(ENC_SALES_FILE) and os.path.getsize(ENC_SALES_FILE) > 0:
        sales_transaction = decrypt_and_return_sales_transactions(
            key, ENC_SALES_FILE
        )
        size = os.path.getsize(ENC_SALES_FILE)
        print(f" Sales loaded from {ENC_SALES_FILE}  —  file size: {size} bytes")

    # Display header on startup
    display_header()

    # Main application loop
    while True:

        choice = menu()

        if choice == "add":
            item_name, item_price, item_quantity = read_item()

            # Keep asking for serial code until valid unique one entered
            while True:
                item_serial_code = input(
                    " Enter 5-character item serial code"
                    " - for the item to be added to the stock:  "
                ).strip()
                if is_unique(item_serial_code, stock):
                    break
                else:
                    print(" Serial code invalid or already exists. Try again.")

            # Save item to stock
            item = [item_name, item_serial_code, item_price, item_quantity]
            stock.append(item)

            # Encrypt and save stock immediately after add
            encrypt_and_save_stock(key, stock, ENC_STOCK_FILE)

        elif choice == "display":
            display_stock(stock)

        elif choice == "search":
            search(stock)

        elif choice == "sales":
            stock_len_before = len(stock)
            sales_len_before = len(sales_transaction)

            sales_transactions(stock, sales_transaction)

            # Encrypt and save both files if sale was successful
            if (len(stock) != stock_len_before or
                    len(sales_transaction) != sales_len_before):
                encrypt_and_save_stock(key, stock, ENC_STOCK_FILE)
                encrypt_and_save_sales_transaction(
                    key, sales_transaction, ENC_SALES_FILE
                )

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