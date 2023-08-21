from inventory import *
from current_date import *
import os
import csv

current_date = CurrentDate(date.today())

class CsvReader:
    def __init__(self, filename):
        self.filename = filename

# this "resets" the day/ deletes the info_today.csv file if it exists
    def reset_date(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Caution!! File: '{self.filename}' has been removed.")
        else:
            #this lets the user know that the file has been created with the current date
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as file:
                    new_current_date = date.today()
                    file.write(str(new_current_date))
                    print(f"You have created a new file")
                    print(f"This is the current date: {new_current_date}")
                    
                    return new_current_date

# This reads the info_today.csv file if it exists
    def read_today(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as today:
                for row in today:
                    return row
        if not os.path.exists(self.filename):
            print("ERROR: File not available")

# this is creating a today date if doesnt exists and put it in a file: info_today.csv
    def create_date_today(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                new_current_date = date.today()
                file.write(str(new_current_date))
                print(f"You have created a new file")
                
                return new_current_date
            
        elif os.path.exists(self.filename):
            with open(self.filename, "r") as changed_file:
                reader = csv.reader(changed_file)
                for line in reader:
                    date_object = datetime.strptime(line[0], "%Y-%m-%d").date()
                    
                    return date_object

# this is changing the date forward in info_today.csv
    def change_forward(self,days):
        current_date = CurrentDate(self.create_date_today())
        if os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write(str(current_date.go_to_the_future(days)))
                print("Caution, the date has been changed")

                return current_date.time()

# this is changing the date backwards(rewind) in info_today.csv
    def change_rewind(self,days):
        current_date = CurrentDate(self.create_date_today())
        if os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write(str(current_date.go_to_the_past(days)))
                print("Caution, the date has been changed")

                return current_date.time()
