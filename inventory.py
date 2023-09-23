import csv
import os
import shutil
import random
from tempfile import NamedTemporaryFile
from rich.console import Console
from rich.traceback import install
from rich import print
from current_date import *
from csv_reader import *
from matplotlib import pyplot as plt

# All the needed variables in the program
install()
console = Console()

class Inventory:

    def __init__(self, filename):
        self.filename = filename

# this shows inventory information 
    def inventory_info(self):
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    print(f"{key}: {value}")

# this shows sales information
    def sales_info(self):
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for key, value in row.items():
                    print(f"{key}: {value}")
            return row

# this shows all products and quantity
    def all_products(self):
        with open(self.filename, "r") as file:
            read = csv.DictReader(file)
            for row in read:
                print(f"Product: {row['product name']}\nQuantity: {row['quantity']}")

# this show the product buy date and expiration date
    def product_bought(self):
        with open(self.filename, "r") as file:
            read = csv.DictReader(file)
            for row in read:
                print(f"Product: {row['product name']}, Buy date {row['buy date']}, Expiration date {row['expiration date']}")

# this shows products sold and if it was expired
    def product_sold(self, info_today): 
        with open(self.filename, "r") as sold:
            check_sold = csv.DictReader(sold)
            for row in check_sold: 
                exp_date = row['expiration date']
                sell_price = row['sell price']
                product = row["product name"]
                if info_today <= exp_date:
                    print(f"{product} was sold for: {sell_price} with expiration date of: {exp_date}")
                else:
                    print(f"[bold red]ERROR:[/bold red] {product} has been expired {exp_date}")

# this is buying a product 
    def buy_product(self, product_name, price, expiration_date, quantity, today):
        fieldnames = ['id', 'product name','buy date','sell price','expiration date','quantity']
        with open(self.filename, "r+", newline="") as buying_prod:
            writer = csv.DictWriter(buying_prod, fieldnames=fieldnames, delimiter=",")
            # checks if the file exists otherwise makes a header and buys the product
            if os.path.exists("inventory.csv") == False:
                writer.writeheader()
                id = 1
                writer.writerow({'id': id, 
                                'product name': product_name,
                                'buy date': today, 
                                'sell price': price, 
                                'expiration date': expiration_date, 
                                'quantity': quantity})
            # This adds it to the final line of the inventory file
            else:
                final_line = buying_prod.readlines()[-1]
                last_line = final_line.split(",")
                id = int(last_line[0]) + 1
                writer.writerow({'id': id, 
                                'product name': product_name,
                                'buy date': today, 
                                'sell price': price, 
                                'expiration date': expiration_date, 
                                'quantity': quantity})

# this is selling a product
    def sell_product(self, product_name, quantity, sold_price):
        filename = "inventory.csv"
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        fieldnames = ['id', 'product name', 'buy date', 'sell price', 'expiration date', 'quantity']

        # checks if file exists and does a status check if the file is empty (== 0)
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            print("[bold red]ERROR:[/bold red] Inventory file is empty or does not exist.")
            return
        # opens the inventory file and the temp file
        with open(self.filename, "r+", newline="") as sell_prod, tempfile:
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames, delimiter=",")
            reader = csv.DictReader(sell_prod, fieldnames=fieldnames, delimiter=",")
            # checks if the product names are equal then the prod_found to True
            if os.path.exists("inventory.csv"):
                prod_found = False # set prod_found to False
                for lines in reader:
                    if product_name == lines["product name"]:
                        prod_found = True
                        product_quantity = lines["quantity"]
                        price_sold = quantity * sold_price

                        # checks if the quantity is more than quantity in inventory
                        if quantity > int(product_quantity):
                            print(f"[bold red]ERROR:[/bold red] Not enough {product_name} in stock. Available quantity: {product_quantity}")
                            return 
                        # this updates the stock if a sale has been made and add it to sales.csv
                        new_stock = int(product_quantity) - quantity
                        print(f"[bold dark_green]-UPDATING STOCK-[/bold dark_green]\nProduct: {lines['product name']}\nQuantity sold: {quantity}\nCurrent quantity: {new_stock}\nPrice sold: {price_sold} dollars")
                        
                        row = {
                            "id": lines["id"],
                            "product name": lines["product name"],
                            "buy date": lines["buy date"],
                            "sell price": sold_price,
                            "expiration date": lines["expiration date"],
                            "quantity": new_stock
                        }
                        self.add_sale_product(row, quantity, sold_price)
                        # if the new stock reaches 0 stop iterating over product and continue
                        if  new_stock == 0:
                            print(f"[bold red]ERROR:[/bold red] {product_name} out of stock, quantity: {new_stock}")
                            continue
                        writer.writerow(row)
                        
                    else:
                        writer.writerow(lines)
                        # when product is not in file send error message
                if prod_found == False:
                    print(f"[bold red]ERROR:[/bold red] Product: {product_name}, not in stock")

            # this makes sure that when product reaches 0 it deletes it from the inventory file
            
            shutil.move(tempfile.name, filename)

    # this add the sold product to the sales.csv
    def add_sale_product(self, sale_record, quantity_sold, sold_price): #add parameter for sold price
        filename = "sales.csv"
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        fieldnames = ["id", "product name", "bought price", "bought id", "sell date", "sell price", "quantity sold"]
        # opening the sales.csv and tempfile
        with open(filename, "r+", newline="") as sales, tempfile:
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames, delimiter=",")
            reader = csv.DictReader(sales, fieldnames=fieldnames, delimiter=",")
            # if inventory product is the same as sales product
            for sale in reader:
                if sale_record["product name"] == sale["product name"]:
                    sale["quantity"] = str(int(sale["quantity sold"]) + quantity_sold)
                    # then update the row
                    writer.writerow({
                        "id": sale_record["id"],
                        "product name": sale["product name"],
                        "bought price": sale["bought price"],
                        "bought id": random.randint(20, 30),
                        "sell date": sale["sell date"],
                        "sell price": sold_price,
                        "quantity sold": sale["quantity"]})
                # write the row again from the sales file
                else:
                    writer.writerow(sale)
                    
        # this makes sure that it updates the sales file
        shutil.move(tempfile.name, filename)
        

# This reports the revenue making sure the date is the same ass the sell date in sales file
    def get_revenue(self, date_today):
        total_sum = 0
        products_sold = {}  # Dictionary to store products and their total prices
        rev_made = False  # set rev_made to False

        with open(self.filename, "r") as revenue:
            reader = csv.DictReader(revenue)
            for row in reader:
                sell_date = row["sell date"]
                product = row["product name"]
                if date_today == sell_date:
                    rev_made = True
                    price = float(row["sell price"])
                    total_sum += price
                    if product in products_sold:
                        products_sold[product] += price
                    else:
                        products_sold[product] = price

        if rev_made:
            print(f"This is today's date: {date_today}")
            print(f"Total revenue: {total_sum}")
            for product, price in products_sold.items():
                print(f"Product sold: {product}, Total price: {price}")
            return total_sum
        else:
            print(f"There is no revenue made as of today: {date_today}")
            return 0  # Return 0 when no revenue is made
            
    # This reports the profit making sure the date is the same ass the sell date in sales file
    def get_profit(self, date_today):
        total_profit = 0
        products_sold = {}  # Dictionary to store products and their profits
        prof_made = False  # set prof_made to False

        with open(self.filename, "r") as profit:
            reader = csv.DictReader(profit)
            for row in reader:
                sell_date = row["sell date"]
                if date_today == sell_date:
                    prof_made = True
                    product = row["product name"]
                    sell_price = float(row["sell price"])
                    bought_price = float(row["bought price"])
                    profit_per_product = sell_price - bought_price
                    total_profit += profit_per_product
                    if product in products_sold:
                        products_sold[product] += profit_per_product
                    else:
                        products_sold[product] = profit_per_product

        if prof_made:
            print(f"This is today's date: {date_today}")
            print(f"Total profit: {total_profit}")
            for product, profit in products_sold.items():
                print(f"Product sold: {product}, Profit: {profit}")
            return total_profit
        else:
            print(f"No profit has been made as of today: {date_today}")
            return 0  # Return 0 when no profit is made

    def get_visualization(self):
        date_prices = {}  # Dictionary to store date as key and prices as values
        with open(self.filename, "r") as sales:
            reader = csv.DictReader(sales)
            for row in reader:
                date = row["sell date"]
                profit = float(row["sell price"]) - float(row["bought price"])
                revenue = float(row["sell price"])
                # checks if the date is in dict date_prices if so add them together else leave it
                if date in date_prices:
                    date_prices[date]["profit"] += profit
                    date_prices[date]["revenue"] += revenue
                else:
                    date_prices[date] = {"profit": profit, "revenue": revenue}
        # with the data found and put in lists put them in variables to use in plot
        dates = list(sorted(date_prices))
        profit_datay = [date_prices[date]["profit"] for date in dates]
        revenue_datay = [date_prices[date]["revenue"] for date in dates]
        #plot methods and information
        plt.style.use("seaborn-v0_8-poster")
        plt.plot(dates, profit_datay, marker="s", linestyle="--", label="Profit")
        plt.plot(dates, revenue_datay, marker="s", linestyle="-", label="Revenue")
        #plot graph titles
        plt.xlabel("Date sold")
        plt.ylabel("Price in dollars")
        plt.title("CSV Data Graph")
        # plot layout
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout() # makes the lay out tighter so its better to read
        
        plt.savefig("CSV Data Graph", format="pdf")  # Save the plot as a PDF file
        plt.show()

