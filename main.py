#FlavourSync, a program originally made by Bhaskar Patel for his school project.

import json, pytz
from datetime import datetime
from tabulate import tabulate
from res_library import get_input as ginput

with open("res_menu.json", encoding = 'utf-8') as f1:
    data = json.load(f1)
    menu = json.dumps(data, indent=4)


def check_weekend():
    india_timezone = pytz.timezone('Asia/Kolkata')
    today = datetime.now(india_timezone).weekday()
    if today < 5:
        return False
    else:
        return True

def add_menu_item(menu_data):
    name = input("Enter the name of the new menu item: ")
    price = float(input("Enter the price of the new menu item: "))
    category = ginput("Enter the category of the new menu item (veg/non-veg/sweets/drinks): ",str,["veg", "non-veg", "sweets", "drinks"], True)
    special = input("Is this a special item for weekends? (y/n): ").lower() == 'y'

    new_item = {
    "name": name,
    "price": price,
    "category": category,
    "special": special    
    }

    menu_data["menu"].append(new_item)

    with open('res_menu.json', 'w', encoding = 'utf-8') as f2:
        json.dump(menu_data, f2, indent=4)
    with open('res_menu.json', encoding = 'utf-8') as f2:
        json.load(f2)

def print_categorized_menu(menu_data,for_order = True):
    categorized_menu = {"veg": [], "non-veg": [], "sweets": [], "drinks": []}

    for item in menu_data["menu"]:
        category = item["category"]
        if item["special"] == True:
            if check_weekend():
                categorized_menu[category].append([item["name"], item["price"], item["code"]])
        else:
            categorized_menu[category].append([item["name"], item["price"], item["code"]])

    table_data = []
    for category, items in categorized_menu.items():
        if items:
            table_data.append([f"{category.capitalize()} Category", ""])
            table_data.extend(items)
            table_data.append([]) #Add an empty row between categories.

    table = tabulate(table_data, headers=["Item", "Price", "Code"], tablefmt="grid")
    print(table)

    if for_order:
        pass

def home():
    chosen_menu = ginput("Enter what you want to see: \n'o' : Order Food\n't' : Track Order\n'm' : Show Menu\n'r' : Table Reservation\n'e' : Employee Management\n'i' : Restaurant Info\n",str,['o','e','i','m','t','r'],True)
    if chosen_menu == 'r':
        reserve()
    elif chosen_menu == 'm':
        print_categorized_menu(data)
        home()
    elif chosen_menu == 'e':
        manage_employees()
    elif chosen_menu == 'o':
        start_order()
    elif chosen_menu == 't':
        tracking()
    elif chosen_menu == 'i':
        info()

def reserve():
    pass

def manage_employees():
    pass

def start_order():
    pass

def tracking():
    pass

def info():
    pass

def main():
    home()

if __name__ == "__main__":
    main()