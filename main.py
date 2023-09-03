#FlavourSync, a program originally made by Bhaskar Patel for his school project.

import json
import pytz
from datetime import datetime as dt
from tabulate import tabulate
from res_library import get_input as ginput

with open("res_menu.json", encoding = 'utf-8') as f1:
    data = json.load(f1)
    menu = json.dumps(data, indent=4)


def check_weekend():
    india_timezone = pytz.timezone('Asia/Kolkata')
    today = dt.now(india_timezone).weekday()
    if today < 5:
        return False
    else:
        return True

def add_menu_item(menu_data):
    name = input("Enter the name of the new menu item: ")
    price = float(input("Enter the price of the new menu item: "))
    category = ginput("Enter the category of the new menu item (veg/non-veg/sweets/drinks): ",str,["veg", "non-veg", "sweets", "drinks"], True)
    code = input("Enter the code of the new item")
    special = input("Is this a special item for weekends? (y/n): ").lower() == 'y'

    new_item = {
    "name": name,
    "price": price,
    "category": category,
    "code": code,
    "special": special
    }

    menu_data["menu"].append(new_item)

    with open('res_menu.json', 'w', encoding = 'utf-8') as f2:
        json.dump(menu_data, f2, indent=4)
    with open('res_menu.json', encoding = 'utf-8') as f2:
        json.load(f2)

def print_categorized_menu(menu_data,for_order = False):
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
        start_order()

def start_order():
    order_list = []
    menu_list = ['done']
    for item in data["menu"]:
        menu_list.append(item["code"].lower())
    while True:
        add_item = ginput("Enter the code of the dish you want to buy (Write 'done' to proceed): ", str, menu_list, True)
        if add_item.lower() == 'done':
            break
        order_list.append(add_item.upper())
        print(order_list)

def home():
    chosen_menu = ginput("Enter what you want to see: \n'o' : Order Food\n't' : Track Order\n'm' : Show Menu\n'r' : Table Reservation\n'e' : Employee Management\n'i' : Restaurant Info\n",str,['o','e','i','m','t','r'],True)
    if chosen_menu == 'r':
        reserve()
    elif chosen_menu == 'm':
        print_categorized_menu(data, False)
        home()
    elif chosen_menu == 'e':
        manage_employees()
    elif chosen_menu == 'o':
        print_categorized_menu(data, True)
    elif chosen_menu == 't':
        tracking()
    elif chosen_menu == 'i':
        info()

def reserve():
    pass

def manage_employees():
    pass

def tracking():
    pass

def info():
    pass

def main():
    home()

if __name__ == "__main__":
    main()