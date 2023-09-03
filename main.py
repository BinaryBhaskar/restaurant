#FlavourSync, a program originally made by Bhaskar Patel for his school project.

import string
import random
import json
import pytz
from datetime import datetime as dt
from tabulate import tabulate
from res_library import get_input as ginput

india_timezone = pytz.timezone('Asia/Kolkata')

with open("res_menu.json", encoding = 'utf-8') as f1:
    data = json.load(f1)
    menu = json.dumps(data, indent=4)

with open('orders_log.json', 'r', encoding = 'utf-8') as o1:
    orders_data = json.load(o1)

def check_weekend():
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
    br()
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
    br()

    if for_order:
        start_order()
    else:
        input("Prese Enter to return to home.")

def start_order():
    order_list = []
    menu_list = ['done']
    menu_data = data['menu']
    for item in menu_data:
        menu_list.append(item["code"].lower())
    while True:
        add_item = ginput("Enter the code of the dish you want to buy (Write 'done' to proceed): ", str, menu_list, True)
        if add_item.lower() == 'done':
            break
        buy_item = next((item for item in menu_data if item["code"].lower() == add_item), None)
        order_list.append(buy_item)
        order_info(order_list)
    order_info(order_list, True)

def order_info(orderedlist,accepted=False):
    br()
    print("  Current Order: ")
    total_price = 0
    for item in orderedlist:
        total_price += item['price']
        print(f"      {item['name']} : {item['price']}")
    print(f'    Total Price : {total_price}')
    br()
    if accepted:
        cancel_continue = ginput("Enter 'cancel' to Cancel or 'pay' to Continue to Payment: ", str, ['cancel', 'pay'], True)
        br()
        if cancel_continue == 'cancel':
            home()
        else:
            name = input("Enter your name here: ")
            address = input("Enter your full address here: ")
            payment_prompt = gen_pay_id(total_price,orderedlist,address,name)
            print(payment_prompt)
            br()
            input("Press Enter to return to home. ")
            home()

def gen_pay_id(vtotal_price, order_details, address, name):
    alphabetical_caps = list(string.ascii_uppercase)
    numerical_digits = [str(i) for i in range(10)]
    bill_id = f"{random.choice(alphabetical_caps)}{random.choice(numerical_digits)}{random.choice(numerical_digits)}{random.choice(numerical_digits)}{dt.now(india_timezone).date()}"
    new_delivery_order = {
        "name": name,
        "order_id": bill_id,
        "price": vtotal_price,
        "order_details": order_details,
        "address": address,
        "payment_status": "NOT PAID",
        "time_of_order": f"{dt.now(india_timezone)}"
    }
    data["deliveries"].append(new_delivery_order)
    with open('orders_log.json', 'w', encoding = 'utf-8') as o2:
        json.dump(orders_data, o2, indent=2)
    print("New delivery order has been added to 'deliveries'.")
    return (f"Please kindly pay your bill at the counter\n  Rs.{vtotal_price}\n  Bill ID: {bill_id}")

def br():
    print("="*70)

def home():
    br()
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

def reserve(from_home = False):
    if from_home:
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
    br()
    print("Welcome to FlavourSync")
    main()