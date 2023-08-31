import json
from datetime import datetime
from tabulate import tabulate


with open('res_menu.json') as f:
    data = json.load(f)
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
    category = input("Enter the category of the new menu item (veg/non-veg/sweets/drinks): ")
    special = input("Is this a special item for weekends? (y/n): ").lower() == 'y'

    new_item = {
    "name": name,
    "price": price,
    "category": category,
    "special": special    
    }

    menu_data["menu"].append(new_item)

    with open('res_menu.json', 'w') as f:
        json.dump(menu_data, f, indent=4)
    with open('res_menu.json') as f:
        data = json.load(f)

def print_categorized_menu(menu_data):
    categorized_menu = {"veg": [], "non-veg": [], "sweets": [], "drinks": []}

    for item in menu_data["menu"]:
        category = item["category"]
        categorized_menu[category].append([item["name"], item["price"]])

    table_data = []
    for category, items in categorized_menu.items():
        if items:
            table_data.append([f"{category.capitalize()} Category", ""])
            table_data.extend(items)
            table_data.append([])  # Add an empty row between categories

    table = tabulate(table_data, headers=["Item", "Price"], tablefmt="grid")
    print(table)


# Call the function to print the categorized menu
print_categorized_menu(data)

#add_menu_item(data)
#print(check_weekend())
#yo