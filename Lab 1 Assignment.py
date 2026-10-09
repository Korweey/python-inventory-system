j"""
------------------------------------------------------------
Application Programming CCGC 5003
Lab 1 - Inventory System (Phase I)
Summer 2026

Developer Name : Qawiyy Rabiu
Student ID     : N10038749

Description:
This program reads item information such as:
- Item Name
- Item Serial Code
- Item Price
- Item Quantity

The information is displayed in a tabular format
using functions and argument passing.
------------------------------------------------------------
"""


# ----------------------------------------------------
# Function Name: display_developer_info
# ----------------------------------------------------
def display_developer_info():
    """
    Displays the developer's/student's name and student ID
    right-aligned on the terminal display.

    Parameters:
        None

    Returns:
        None
    """
    print(f"{'Student Name: Qawiyy Rabiu':>100}")
    print(f"{'Student ID:   N10038749':>100}\n")


# ----------------------------------------------------
# Function Name: read_item_info
# ----------------------------------------------------
def read_item_info():
    """
    Prompts the user to enter item information including
    item name, serial code, price, and quantity.

    Parameters:
        None

    Returns:
        tuple: (item_name: str, serial_code: str,
                item_price: float, item_quantity: int)
    """
    item_name     = input("Enter Item Name:\t ")
    serial_code   = input("Enter Item Serial Code:\t ")
    item_price = float(input("Enter Item Price:  $ ").replace(",", ""))
    item_quantity = int(input("Enter Item Quantity:\t "))

    return item_name, serial_code, item_price, item_quantity


# ----------------------------------------------------
# Function Name: display_item_info
# ----------------------------------------------------
def display_item_info(item_name, serial_code, item_price, item_quantity):
    """
    Displays the item information in a formatted tabular layout.
    The heading row and data row are both right-aligned.
    The item price is displayed with a '$' symbol.

    Parameters:
        item_name     (str)   : The name of the item
        serial_code   (str)   : The serial code of the item
        item_price    (float) : The price of the item
        item_quantity (int)   : The quantity of the item

    Returns:
        None
    """
    print("\n")
    print("-" * 90)

    # Table heading
    print(f"{'Item Name': >22}"
          f"{'Item Serial Code':>25}"
          f"{'Item Price': >20}"
          f"{'Item Quantity': >20}")

    print("-" * 90)

    # Table data row — price displayed with '$' symbol
    print(f"{item_name:>22}"
          f"{serial_code:>25}"
          f"{'$ ' + f'{item_price:.2f}':>20}"
          f"{item_quantity:>20}")

    print("-" * 90)


# ----------------------------------------------------
# Function Name: main
# ----------------------------------------------------
def main():
    """
    Main application function. Orchestrates the program flow by:
      1. Displaying developer information
      2. Reading item data from the user and saving values
         in appropriate data types
      3. Passing the collected values to the display function

    Parameters:
        None

    Returns:
        None
    """
    # Display developer information
    display_developer_info()

    # Read item information and save in respective data types
    item_name, serial_code, item_price, item_quantity = read_item_info()

    # Display item information in tabular format
    display_item_info(item_name, serial_code, item_price, item_quantity)


# -------- MAIN APPLICATION --------
if __name__ == "__main__":
    main()