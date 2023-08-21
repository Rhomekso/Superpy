#### With these three technical elements for the superpy assignment i have chosen to put everything in three different classes. This for easier readability and structured code. That way i can always backtrace the code and make sure that if i can and make any improvements i know where to look and adjust the code properly.

## inventory class
This is a long file of code wich is put in an inventory class, this allows me to see each and every part of the code for the inventory. From inventory stock information to revenue and profit information.
Also i implemented a way that when the command is being called by the user for a clear visualization it puts it in a **graph** and in a **pdf file**. 

Making sure it is clear and structured.
I chose to do it this way so i can work along with the other classes 

## current_date class

This file is a base that i use for the files that need the specific information on a specific date or work with the date time module. 
I chose to make sure it counts and calculates on the days that are given by the user, this way there is an easier understanding of what is going on.

## csv_reader class
This file is the base that read the csv files that exists in the superpy directory. Working with the inventory.csv, sales.csv and eventually info_today.csv. I can easily show what is in that file in an ordered and structered manner. Even implementing a reset button so we can always start from scratch/beginning.

## Lastly: main.py 
In this file everything comes together making sure that it gives clear way and visual in the command line interface. That at one point when the user gives the command it clearly gives them the information needed that is being asked.

My choice for all this is to make sure the files are still separate and and easy accessible in the future if changes are to be made.

## In short:
**main.py** is the file that we are working from, 
**inventory.py** is all of the information needed to show the inventory information as well as the sales information.
**current_date.py** sets up the date that i can work with and adjust if needed,
**csv_reader.py** makes sure that i can acces the files that i am working with. Making sure that i can acces the information that is needed for a specific situation.