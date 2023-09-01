#Bytebite, a program originally made by Bhaskar Patel for his school project.

import json
from datetime import datetime
from tabulate import tabulate
from res_library import get_input as ginput

with open("res_menu.json", encoding = 'utf-8') as f1:
    data = json.load(f1)
    menu = json.dumps(data, indent=4)

def check_weekend():
    today = datetime.today().weekday()
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


def print_categorized_menu(menu_data):
    categorized_menu = {"veg": [], "non-veg": [], "sweets": [], "drinks": []}

    for item in menu_data["menu"]:
        category = item["category"]
        if item["special"] == True:
            if check_weekend():
                categorized_menu[category].append([item["name"], item["price"]])
        else:
            categorized_menu[category].append([item["name"], item["price"]])

    table_data = []
    for category, items in categorized_menu.items():
        if items:
            table_data.append([f"{category.capitalize()} Category", ""])
            table_data.extend(items)
            table_data.append([]) #Add an empty row between categories.

    table = tabulate(table_data, headers=["Item", "Price"], tablefmt="grid")
    print(table)


def main():
    print(check_weekend())
    print_categorized_menu(data)
    #add_menu_item(data)
    #print_categorized_menu(data)


if __name__ == "__main__":
    main()
