import csv
import os
import shutil
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

# use a boolean that checks if a product is sold (sold = True) then make sure to append it to the sales.csv
# also check if the product sold == product sales list and quantity is < quantity in sales list and then append the product sold to the product list (product sold += product in sales list)
    def sell_product(self, product_name, quantity):
        filename = "inventory.csv"
        # sales_file = "sales.csv" TODO
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        fieldnames = ['id', 'product name', 'buy date', 'sell price', 'expiration date', 'quantity']
        # sales_fieldnames = ["id","product name","bought price","bougt id","sell date","sell price","quantity sold"]TODO

        # checks if file exists and does a status check if the file is empty (== 0)
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            print("ERROR: Inventory file is empty or does not exist.")
            return
        
        with open(self.filename, "r+", newline="") as sell_prod, tempfile:
            writer = csv.DictWriter(tempfile, fieldnames=fieldnames, delimiter=",")
            reader = csv.DictReader(sell_prod, fieldnames=fieldnames, delimiter=",")
            # sales_writer = csv.DictWriter(sales_file, fieldnames=sales_fieldnames, delimiter=",")TODO

            if os.path.exists("inventory.csv"):
                prod_found = False
                # sold = False TODO
                for lines in reader:
                    if product_name == lines["product name"]:
                        prod_found = True
                        product_quantity = lines["quantity"]

                        # checks if the quantity is more than quantity in inventory
                        if quantity > int(product_quantity):
                            print(f"ERROR: Not enough {product_name} in stock. Available quantity: {product_quantity}")
                            return 
                        
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
                    else:
                        writer.writerow(lines)
                        # when product is not in file send error message
                if prod_found == False:
                    print(f"ERROR product: {product_name}, not in stock")

            # this makes sure that when product reaches 0 it deletes it from the inventory file
            shutil.move(tempfile.name, filename)


    def add_sale_product(self,sale_record ):
        filename = "sales.csv"
        fieldnames = "id","product name","bought price","bougt id","sell date","sell price"
        with open(self.filename, "a", newline="") as sales:
            writer = csv.DictWriter(filename, fieldnames=fieldnames, delimiter=",")
            writer.writerow(sale_record)

# This reports the revenue making sure the date is the same ass the sell date in sales file
    def get_revenue(self, date_today):
        total_sum = 0
        products_sold = {}  # Dictionary to store products and their total prices
        rev_made = False  # Initialize rev_made to False

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
        prof_made = False  # Initialize prof_made to False

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
        plt.ylabel("Price")
        plt.title("CSV Data Graph")
        # plot layout
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout() # makes the lay out tighter so its better to read
        
        plt.savefig("CSV Data Graph", format="pdf")  # Save the plot as a PDF file
        plt.show()

