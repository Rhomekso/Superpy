import csv
import os
import shutil
from tempfile import NamedTemporaryFile
from rich.console import Console
from rich.traceback import install
from rich import print
from datetime import datetime
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
                print(f"This is the buy date {row['buy date']}, Expiration date {row['expiration date']}")

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
                    print(f"ERROR: {product} has been expired {exp_date}")

# this is buying a product 
    def buy_product(self, product_name, price, expiration_date, quantity, today):
        fieldnames = ['id', 'product name','buy date','sell price','expiration date','quantity']
        with open(self.filename, "r+", newline="") as buying_prod:
            writer = csv.DictWriter(buying_prod, fieldnames=fieldnames, delimiter=",") 
            if os.path.exists("inventory.csv") == False:
                writer.writeheader()
                id = 1
                writer.writerow({'id': id, 
                                'product name': product_name,
                                'buy date': today, 
                                'sell price': price, 
                                'expiration date': expiration_date, 
                                'quantity': quantity})
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
    def sell_product(self, product_name, quantity):
        filename = "inventory.csv"
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        fieldnames = ['id', 'product name', 'buy date', 'sell price', 'expiration date', 'quantity']
        with open(self.filename, "r+", newline="") as sell_prod, tempfile:
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames, delimiter=",")
            reader = csv.DictReader(sell_prod, fieldnames=fieldnames, delimiter=",")
            if os.path.exists("inventory.csv"):
                prod_found = False
                for lines in reader:
                    if product_name == lines["product name"]:
                        prod_found = True
                        product_quantity = lines["quantity"]
                        new_stock = int(product_quantity) - quantity
                        print(f"-Updating stock-\nproduct: {lines['product name']}\nquantity sold: {quantity}\ncurrent quantity: {new_stock}")
                        row = {
                            "id": lines["id"],
                            "product name": lines["product name"],
                            "buy date": lines["buy date"],
                            "sell price": lines["sell price"],
                            "expiration date": lines["expiration date"],
                            "quantity": new_stock
                        }
                        # if the new stock reaches 0 stop iterating over product and continue
                        if  new_stock == 0:
                            print(f"{product_name} out of stock, quantity: {new_stock}")
                            continue
                        writer.writerow(row)
                        # this makes sure the file stays intact and moves to the last if statement
                    else:
                        row = {
                            "id": lines["id"],
                            "product name": lines["product name"],
                            "buy date": lines["buy date"],
                            "sell price": lines["sell price"],
                            "expiration date": lines["expiration date"],
                            "quantity": lines["quantity"]
                        }
                        writer.writerow(lines)
                        # when product is not in file send error message
                if prod_found == False:
                    print(f"ERROR product: {product_name}, not in stock")
            shutil.move(tempfile.name, filename)

# This reports the revenue making sure the date is the same ass the sell date in sales file
    def get_revenue(self,date_today):
        total_sum = 0
        rev_made = True
        with open(self.filename, "r") as revenue:
            reader = csv.DictReader(revenue)
            for row in reader:
                sell_date = row["sell date"]
                if date_today == sell_date:
                    rev_made = True
                    price = float(row["sell price"])
                    total_sum += price
            if rev_made == True:
                    print(f"This is today's date: {date_today}")
                    print(f"Total revenue: {total_sum}")
                    
            else:
                rev_made = False
                if rev_made == False:
                    print(f"There is no revenue made as of today: {date_today}")

                return total_sum
            
# This reports the profit making sure the date is the same ass the sell date in sales file
    def get_profit(self, date_today):
        total_profit = 0 
        prof_made = True
        with open(self.filename, "r") as profit:
            reader = csv.DictReader(profit)
            for row in reader:
                sell_date = row["sell date"]
                if date_today == sell_date:
                    prof_made = True
                    caculate_profit = float(row["sell price"]) - float(row["bought price"])
                    total_profit += caculate_profit
            if prof_made == True:
                print(f"This is today's date: {date_today}")
                print(f"Total profit: {total_profit}")
            else:
                prof_made = False
                if prof_made == False:
                    print(f"No profit has been made as of today: {date_today}")

            return total_profit

    def get_visualization(self):
        date_prices = {}  # Dictionary to store date as key and prices as values
        
        with open(self.filename, "r") as sales:
            reader = csv.DictReader(sales)
            for row in reader:
                date = row["sell date"]
                profit = float(row["sell price"]) - float(row["bought price"])
                revenue = float(row["sell price"])
                
                if date in date_prices:
                    date_prices[date]["profit"] += profit
                    date_prices[date]["revenue"] += revenue
                else:
                    date_prices[date] = {"profit": profit, "revenue": revenue}
        
        dates = list(date_prices.keys()) #keys() return a view object of the dict as a list
        profit_datay = [date_prices[date]["profit"] for date in dates]
        revenue_datay = [date_prices[date]["revenue"] for date in dates]
        
        plt.plot(dates, profit_datay, marker="o", linestyle="-", label="Profit")
        plt.plot(dates, revenue_datay, marker="o", linestyle="-", label="Revenue")
        
        plt.xlabel("Date sold")
        plt.ylabel("Price")
        plt.title("CSV Data Graph")
        
        plt.legend()
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        
        plt.show()

