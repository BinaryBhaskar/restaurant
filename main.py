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


def get_input(prompt, given_type, range = []):
    while True:
        value = input(prompt)
        if type(value) == given_type:
            pass
        elif given_type == int:
            try:
                value = int(value)
                pass
            except ValueError:
                print("Invalid Response, please re-enter value.")
                continue
        if (range == []) or (range != [] and value in range):
            return value
        else:
            print("Invalid Response, please re-enter value.")
            continue

#get_input("y: ", int, range(40))
# Call the function to print the categorized menu
print_categorized_menu(data)

#add_menu_item(data)
#print(check_weekend())