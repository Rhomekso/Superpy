# Imports
import argparse
from rich import print
from inventory import *


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
INVENTORY_FILE = "inventory.csv"
SALES_FILE = "sales.csv"

# Header
parser = argparse.ArgumentParser(description="Supermarket information tool")

# CLI for product information
parser.add_argument("--all_prod", action="store_true", help="shows all products and quantity")
parser.add_argument("--bought", action="store_true", help="shows all bought products and expiration date")
parser.add_argument("--sold", action="store_true", help="shows product price and expiration date or if it is expired.")
parser.add_argument("--inven", action="store_true", help="shows product inventory stock information")
parser.add_argument("--sales", action="store_true", help="shows product sales information")
parser.add_argument("--revenue", action="store_true", help="shows revenue information")
parser.add_argument("--reset", action="store_true", help="resets and deletes date file")
parser.add_argument("--profit", action="store_true", help="shows profit information")
parser.add_argument("--get_viz", action="store_true", help="shows visual information in a graph")

# Command input
subparsers = parser.add_subparsers(dest="command", help="Information on adjusting the data")

subparser_date = subparsers.add_parser("create", help="This creates date of today")

# CLI for the date of today
subparser_date = subparsers.add_parser("today", help="This shows today's date")

# CLI for the set date 
subparser_set = subparsers.add_parser("set", help="This sets the date")
subparser_set.add_argument("--date", help="set date(YYYY-MM-DD)", type=str, required=True)

# CLI for the date of forward
subparser_forward = subparsers.add_parser("forward",help="Jumping forward")
subparser_forward.add_argument("--add", help="add days (DD)", type=int, required=True)

# CLI for the date of rewind
subparser_rewind = subparsers.add_parser("rewind", help="Hopping back")
subparser_rewind.add_argument("--sub", help="subtract days (DD)", type=int, required=True)

# CLI for the buy parser
subparser_buy = subparsers.add_parser("buy", help="Buying a product")
subparser_buy.add_argument("--product", help="wich product", type=str, required=True)
subparser_buy.add_argument("--price", help="product price", type=float, required=True)
subparser_buy.add_argument("--quantity", help="desired quantity", type=int, required=True)
subparser_buy.add_argument("--expiration", help="expiration date", type=str, required=True)

# CLI for the sell parser
subparser_sell = subparsers.add_parser("sell", help="Selling a product")
subparser_sell.add_argument("--product", help="wich product", type=str, required=True)
subparser_sell.add_argument("--quantity", help="desired quantity", type=int, required=True)

args = parser.parse_args()

# create an usage guide
# using the argparse module to add arguments and sub arguments to make sure the help information is clear and readable

if __name__ == "__main__":
    
    csv_reader = CsvReader("info_today.csv")
    inventory = Inventory(INVENTORY_FILE)
    sales = Inventory(SALES_FILE)

    if args.command == "today": 
        info_today = csv_reader.read_today()

# this shows todays date 
    if args.command == "create": 
        info_today = csv_reader.create_date_today()
        print(f"This is the current date: {info_today}")

    if args.command == "set":
        set_date = args.date
        set_today = csv_reader.set_current_date(set_date)
        print(f"The date has been set to {set_today}")

# This lets you jump forward in days 
    if args.command == "forward":
        days_forward = args.add
        info_forward = csv_reader.change_forward(days_forward)
        print(f"The date has been changed by {days_forward} day(s)")
        print(f"Now we are jumping 'forward': {info_forward}")

# This lets you jump backwards/rewind days 
    if args.command == "rewind":
        days_rewind = args.sub
        info_today = csv_reader.create_date_today()
        current_date = CurrentDate(info_today)
        rewind_output = current_date.go_to_the_past(days_rewind)
        info_rewind = csv_reader.change_rewind(days_rewind)
        print(f"The date has been changed by {days_rewind} day(s)")
        print(f"With this we are going to 'rewind' time: {rewind_output}")

# Buying a product also adds it to file if it doesnt exists 
    if args.command == "buy":
        prod_name = args.product
        price = args.price 
        exp_date = args.expiration
        quant = args.quantity
        today = csv_reader.create_date_today()
        prod_buy = inventory.buy_product(prod_name, price, exp_date, quant, today)
        print("The following has been bought.")
        print(f"Product: {prod_name}, Price: {price}, Expiration date: {exp_date}, Quantity: {quant}")

# Sells the product if there is enough stock 
    if args.command == "sell":
        prod_quantity = args.quantity
        prod_name = args.product
        prod_sell = inventory.sell_product(prod_name, prod_quantity)

# shows inventory information
    if args.inven:
        inventory_stock = inventory.inventory_info()

# show sales information
    if args.sales:
        sales_stock = sales.sales_info()

# shows available products
    if args.all_prod:
        inventory.all_products()

# shows bought products
    if args.bought:
        inventory.product_bought()

# shows products sold
    if args.sold:
        inventory.product_sold(str(csv_reader.create_date_today()))

# reports the revenue on certain dates
    if args.revenue:
        sales.get_revenue(str(csv_reader.read_today()))

# reports the profit 
    if args.profit:
        sales.get_profit(str(csv_reader.read_today()))

# makes a full reset of the date 
    if args.reset:
        csv_reader.reset_date()


    if args.get_viz:
        sales.get_visualization()
