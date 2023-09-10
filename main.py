#FlavourSync, a program originally made by Bhaskar Patel for his school project.

import string #To get letters A-Z and a-z
import random #For generating OrderID
import json
import pytz
import sys
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime as dt
from tabulate import tabulate


india_timezone = pytz.timezone('Asia/Kolkata')
passkey = 'AdminB09'
chandrapur_lat = 21.7067
chandrapur_lon = 83.2325


with open("res_menu.json", encoding = 'utf-8') as f1:
    menudata = json.load(f1) #Menu Data
    menu = json.dumps(menudata, indent=4)

with open('orders_log.json', 'r', encoding = 'utf-8') as o1:
    orderdata = json.load(o1) #Orders Data

def check_weekend():
    today = dt.now(india_timezone).weekday()
    if today < 5:
        return False #If not Weekend
    else:
        return True #If Weekend

def add_menu_item(menu_data): #Add new Item to Menu
    nameslist = [item['name'] for item in menu_data["menu"]]
    codeslist = [item['code'] for item in menu_data["menu"]]
    while True:
        name = input("Enter the name of the new menu item: ").title()
        if name in nameslist:
            print("Item already exists.")
            continue
        else:
            break
    price = float(input("Enter the price of the new menu item: "))
    category = ginput("Enter the category of the new menu item (veg/non-veg/sweets/drinks): ",str,["veg", "non-veg", "sweets", "drinks"], True)
    while True:
        code = input("Enter the code of the new item: ").upper()
        if code in codeslist:
            print("Code already exists.")
            continue
        else:
            break
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
            if check_weekend() or for_order == False:
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
        option = ginput("Prese 'a' to add new item\nor press 'u' to update existing item\nor 'd' to delete an item\nor press anything to return to home:\n",str,[],True)
        if option in ['a', 'd','u'] :
            is_admin = admin_access()
            if is_admin:
                nameslist = [item['name'] for item in menu_data["menu"]]
                codeslist = [item['code'] for item in menu_data["menu"]]
                codeslistlower = [code.lower() for code in codeslist]
                if option == 'a':
                    add_menu_item(menudata)
                elif option == 'u':
                    code = ginput("Enter the code of the item to update: ",str,codeslistlower, True)
                    if code in codeslistlower:
                        all_items = [item for item in menudata["menu"]]
                        itemchosen = [item for item in all_items if item["code"].lower() == code]
                        if itemchosen != None:
                            nameslist.remove(itemchosen[0]["name"])
                            codeslistlower.remove(itemchosen[0]["code"].lower())
                    while True:
                        name = input("Enter the new name of the menu item: ").title()
                        if name in nameslist:
                            print("Item already exists.")
                            continue
                        else:
                            break
                    while True:
                        try:
                            price = float(input("Enter the new price of the menu item: ")) 
                        except ValueError:
                            print("Please enter a floating value.")
                            continue
                        else:
                            break
                    while True:
                        new_code = input("Enter the new code of the item: ").lower()
                        if new_code in codeslistlower:
                            print("Code already exists.")
                            continue
                        else:
                            break
                    update(menudata,code.upper(), name.title(), price, new_code.upper())
                elif option == 'd':
                    codeslistlower = [item['code'].lower() for item in menu_data["menu"]]
                    code = ginput("Enter the code of the item to delete: ",str,codeslistlower, True)
                    delitem(menudata, code.upper())
            else:
                print("You don't have access.")
                home()
        else:
            home()

def update(menu_data, code, new_name, new_price, new_code):
    for item in menu_data["menu"]:
        if item["code"] == code:
            item["name"] = new_name
            item["price"] = new_price
            item["code"] = new_code
            with open('res_menu.json', 'w', encoding='utf-8') as f2:
                json.dump(menu_data, f2, indent=4)
            print("Data changed successfully.")

def delitem(menu_data, code):
    for item in menu_data["menu"]:
        if item["code"] == code:
            menu_data["menu"].remove(item)
            with open('res_menu.json', 'w', encoding='utf-8') as f2:
                json.dump(menu_data, f2, indent=4)
                print("Data deleted successfully")

def admin_access():
    inkey = input("Enter your Passkey: ")
    if inkey == passkey:
        return True
    else:
        return False

def start_order():
    order_list = []
    menu_list = ['done']
    menu_data = menudata['menu']
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

def ginput(prompt, given_type, in_range, do_lower):
    while True:
        value = input(prompt)
        if type(value) == given_type:
            if do_lower:
                value = value.lower()
        elif given_type == int:
            try:
                value = int(value)
            except ValueError:
                print("Invalid Response, please re-enter value.")
                continue
        if (in_range == []) or (in_range != [] and value in in_range):
            return value
        else:
            print("Invalid Response, please re-enter value.")
            continue

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
            while True:
                address = input("Enter your full address here: ").strip()
                if address == "":
                    print("Enter a valid address: ")
                else:
                    geolocator = Nominatim(user_agent="distance_calculator")
                    user_location = geolocator.geocode(address)
                    if user_location:
                        # Extract user's latitude and longitude
                        user_lat = user_location.latitude
                        user_lon = user_location.longitude
                        # Calculate the distance
                        distance_km = distance(chandrapur_lat, chandrapur_lon, user_lat, user_lon)
                        if distance_km > 35:
                            br()
                            toofar = ginput(f"The distance between our restaurant at Chandrapur is too far ({distance_km:.2f}km is more than 35km) from your location.\n   Please try something from the following:\n      'a' to re-enter address\n      'x' to cancel order\n", str, ["a","x"], True)
                            if toofar == "x":
                                print("Order Cancelled")
                                br()
                                input("Press Enter to return to home. ")
                                home()
                            elif toofar == "a":
                                continue
                        break
                    else:
                        print(f"Could not find coordinates for {address}. Please provide a valid address.")
                        continue
            br()
            payment_prompt = gen_pay_id(total_price,orderedlist,address,name)
            print(payment_prompt)
            br()
            input("Press Enter to return to home. ")
            home()

def distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    earth_radius = 6371.0
    distancev = earth_radius * c
    return distancev


def gen_pay_id(vtotal_price, order_details, address, name):
    alphabetical_caps = list(string.ascii_uppercase)
    numerical_digits = [str(i) for i in range(10)]
    all_orders = [order['order_id'] for order in orderdata['deliveries']]
    while True:
        bill_id = f"{random.choice(alphabetical_caps)}{random.choice(numerical_digits)}{random.choice(numerical_digits)}{random.choice(numerical_digits)}_{dt.now(india_timezone).strftime('%d-%m')}"
        if bill_id not in all_orders:
            break
    new_delivery_order = {
        "name": name,
        "order_id": bill_id,
        "price": vtotal_price,
        "order_details": order_details,
        "address": address,
        "time_of_order": f"{dt.now(india_timezone).strftime('%d/%m/%Y, %A, %H:%M')}"
    }
    orderdata["deliveries"].append(new_delivery_order)
    with open('orders_log.json', 'w', encoding = 'utf-8') as o2:
        json.dump(orderdata, o2, indent=2)
    print("New delivery order has been added to 'deliveries'.\nYour order should be delivered to you within 30 minutes.")
    return (f"Please kindly pay your bill during delivery.\n  Rs.{vtotal_price}\n  Bill ID: {bill_id}")

def br():
    print("="*70)

def home():
    br()
    chosen_menu = ginput("Enter what you want to see: \n'o' : Order Food\n't' : Track Orders\n'm' : Show Menu\n'exit' : Exit Program\n" ,str,['o','m','t','exit'],True)
    if chosen_menu == 'm':
        print_categorized_menu(menudata, False)
        home()
    elif chosen_menu == 'o':
        print_categorized_menu(menudata, True)
    elif chosen_menu == 't':
        tracking()
    elif chosen_menu == 'exit':
        sys.exit()

def tracking():
    br()
    all_orders = [order['order_id'] for order in orderdata['deliveries']]
    orders_and_all = all_orders+['all']
    get_id = ginput("Enter your Order ID here (Enter 'all' to see all):  ", str, orders_and_all, False)
    if get_id == 'all':
        for item_id in all_orders:
            br()
            get_order_info(item_id)
    else:
        br()
        get_order_info(get_id)
    br()
    input("Enter to go to home.")
    home()

def get_order_info(order_id_input):
    index = next((i for i, delivery in enumerate(orderdata["deliveries"]) if delivery["order_id"] == order_id_input), None)
    ordered_by = orderdata['deliveries'][index]['name']
    order_value = orderdata['deliveries'][index]['price']
    ordered_items = [item['name'] for item in orderdata['deliveries'][index]['order_details']]
    order_time = orderdata['deliveries'][index]['time_of_order']
    print(f"Order ID: {order_id_input}\nOrdered By: {ordered_by}\nTotal price: {order_value}\nTime of Order: {order_time}\nOrdered Items:{ordered_items}")

def main():
    home()

if __name__ == "__main__":
    br()
    print("Welcome to FlavourSync")
    main()