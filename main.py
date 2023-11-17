#FlavourSync, a program originally made by Bhaskar Patel for his school project.



import sys #To exit program smoothly
from datetime import datetime as dt #To fetch date time data for deliveries and showing menu
import string #To get ASCII letters
import difflib #To compare strings
import random #For generating OrderID
import json #To read/write menu and orders files
import pytz #To get India Timezone
from tabulate import tabulate #To show menu in a tabular form


india_timezone = pytz.timezone('Asia/Kolkata')
passkey = 'AdminB09' #This is the password required to change the menu items or see all orders


if len(sys.argv) > 1: #If program was stared as Admin, don't ask for passkey
    if sys.argv[1] == passkey:
        super_access = True
        print("Started Program as Admin")
    else:
        super_access = False
else:
    super_access = False

with open("res_menu.json", encoding = 'utf-8') as f1: #Open Menu file
    menudata = json.load(f1)
    menu = json.dumps(menudata, indent=4)

with open('orders_log.json', 'r', encoding = 'utf-8') as o1: #Open Orders file
    orderdata = json.load(o1)


def check_weekend():
    today = dt.now(india_timezone).weekday()
    if today < 5:
        return False #If not Weekend, don't show Special Items
    else:
        return True #If Weekend, show Special Items


def add_menu_item(menu_data): #Add new Item to Menu
    nameslist = [item['name'] for item in menu_data["menu"]]
    codeslist = [item['code'] for item in menu_data["menu"]]

    while True: #Get proper, non conflicting Item Name
        name = input("Enter the name of the new menu item: ").title()
        if name in nameslist:
            print("Item already exists.")
            continue
        else:
            break

    while True: #Get Price of New Item
        try:
            price = float(input("Enter the new price of the menu item: "))
        except ValueError:
            print("Please enter a floating value.")
            continue
        else:
            break

    category = ginput("Enter the category of the new menu item (veg/non-veg/sweets/drinks): ",str,["veg", "non-veg", "sweets", "drinks"], True)

    while True: #Get proper, non conflicting Item Code
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

    menu_data["menu"].append(new_item) #Add New Item to Menu

    with open('res_menu.json', 'w', encoding = 'utf-8') as f2: #Store New Menu Data
        json.dump(menu_data, f2, indent=4)
    with open('res_menu.json', encoding = 'utf-8') as f2: #Open New Menu Data for read
        json.load(f2)


def print_categorized_menu(menu_data,for_order = False): #Code to print Menu according to their categories
    br()

    categorized_menu = {"veg": [], "non-veg": [], "sweets": [], "drinks": []} #Initially have empty menu

    for item in menu_data["menu"]: #Add all menu items to their respective categories
        category = item["category"]
        if item["special"]:
            if check_weekend() or not for_order: #Show Special Items if its Weekend or menu has been called from Menu option
                categorized_menu[category].append([item["name"], item["price"], item["code"]])
        else: #Don't show Special Items if it's not weekend and menu was called from Order option
            categorized_menu[category].append([item["name"], item["price"], item["code"]])

    table_data = [] #Initially make an empty table for the menu

    for category, items in categorized_menu.items(): #Fill the table
        if items:
            table_data.append([f"{category.capitalize()} Category", ""])
            table_data.extend(items)
            table_data.append([]) #Add an empty row between categories.

    table = tabulate(table_data, headers=["Item", "Price", "Code"], tablefmt="grid")
    print(table) #Finally, print the Menu as a table
    br()

    if for_order: #If menu shown during order, show ordering options
        start_order()
    else: #If menu shown from Menu option, show menu editing options
        option = ginput("Prese 'a' to add new item\nor press 'u' to update existing item\nor 'd' to delete an item\nor press anything to return to home:\n",str,[],True)
        if option in ['a', 'd','u'] :
            is_admin = admin_access()
            if is_admin:
                nameslist = [item['name'] for item in menu_data["menu"]]
                codeslist = [item['code'] for item in menu_data["menu"]]
                codeslistlower = [code.lower() for code in codeslist]

                if option == 'a': #Add New Item
                    add_menu_item(menudata)

                elif option == 'u':#Update existing Item
                    code = ginput("Enter the code of the item to update: ",str,codeslistlower, True) #Code of Item to Update
                    if code in codeslistlower:
                        all_items = [item for item in menudata["menu"]]
                        itemchosen = [item for item in all_items if item["code"].lower() == code]
                        if itemchosen is not None: #Remove names of chosen Item to handle same name/code conflict if name/code aren't being changed
                            nameslist.remove(itemchosen[0]["name"])
                            codeslistlower.remove(itemchosen[0]["code"].lower())

                    while True: #Get new, non conflicting name
                        name = input("Enter the new name of the menu item: ").title()
                        if name in nameslist:
                            print("Item already exists.")
                            continue
                        else:
                            break

                    while True: #Get New Price
                        try:
                            price = float(input("Enter the new price of the menu item: "))
                        except ValueError:
                            print("Please enter a floating value.")
                            continue
                        else:
                            break

                    while True: #Get new, non conflicting code
                        new_code = input("Enter the new code of the item: ").lower()
                        if new_code in codeslistlower:
                            print("Code already exists.")
                            continue
                        else:
                            break

                    update(menudata,code.upper(), name.title(), price, new_code.upper())

                elif option == 'd': #Delete an existing item from the Menu
                    codeslistlower = [item['code'].lower() for item in menu_data["menu"]]
                    code = ginput("Enter the code of the item to delete: ",str,codeslistlower, True)
                    delitem(menudata, code.upper())
            else:
                print("You don't have access.")
                home()
        else:
            home()


def update(menu_data, code, new_name, new_price, new_code): #Override old data with new data
    for item in menu_data["menu"]:
        if item["code"] == code:
            item["name"] = new_name
            item["price"] = new_price
            item["code"] = new_code
            with open('res_menu.json', 'w', encoding='utf-8') as f2:
                json.dump(menu_data, f2, indent=4)
            print("Data changed successfully.")


def delitem(menu_data, code): #Delete item by its code
    for item in menu_data["menu"]:
        if item["code"] == code:
            menu_data["menu"].remove(item)
            with open('res_menu.json', 'w', encoding='utf-8') as f2:
                json.dump(menu_data, f2, indent=4)
                print("Data deleted successfully")


def admin_access(): #Checks admin access through passkey
    if super_access:
        return True
    inkey = input("Enter your Passkey: ")
    clear()
    if inkey == passkey:
        return True
    else:
        return False


def start_order(): #Ordering mechanism
    order_list = []
    menu_list = ['done']
    for item in menudata['menu']:
        menu_list.append(item["code"].lower())
    while True:
        add_item = ginput("Enter the code of the dish you want to buy (Write 'done' to proceed): ", str, menu_list, True)
        if add_item.lower() == 'done':
            sys.stdout.write('\033[2J')
            break
        buy_item = next((item for item in menudata['menu'] if item['code'].lower() == add_item), None)
        order_list.append(buy_item)
        order_info(order_list)
    order_info(order_list, True)

def clear():
    sys.stdout.write('\033[2J')
    sys.stdout.flush()

def ginput(prompt, given_type, in_range, do_lower): #Get accurate input of a given type and in a range of values
    while True:
        value = input(prompt)
        if type(value) == given_type:
            if do_lower:
                value = value.lower()
        elif given_type == int:
            try:
                value = int(value)
            except ValueError:
                br()
                print("Invalid Response, please re-enter value.")
                br()
                continue
        if (in_range == []) or (in_range != [] and value in in_range):
            return value
        else:
            closest_match = difflib.get_close_matches(value, in_range)
            if closest_match:
                meant = input(f'"{value}" not found. Did you mean "{closest_match[0]}"? ("y/n"): ').strip().lower()
                if meant == "y":
                    value = closest_match[0]
                    return value
            else:
                br()
                print("Invalid Response, please re-enter value.")
                br()
            continue


def order_info(orderedlist,accepted=False): #Show current order info and price, and continue to pay or cancel
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
            while True:
                name = input("Enter your name here: ").strip().title()
                if name == "":
                    print("Enter a valid name: ")
                else:
                    break
            while True:
                address = input("Enter your full address here: ").strip()
                if address == "":
                    print("Enter a valid address: ")
                else:
                    break
            br()
            payment_prompt = gen_pay_id(total_price,orderedlist,address,name)
            print(payment_prompt)
            br()
            input("Press Enter to return to home. ")
            home()


def gen_pay_id(vtotal_price, order_details, address, name): #Generate a non conflicting Order ID and add the order info to Orders file
    alphabetical_caps = list(string.ascii_uppercase)
    numerical_digits = [str(i) for i in range(10)]
    all_orders = [order['order_id'] for order in orderdata['deliveries']]
    while True:
        bill_id = f"{random.choice(alphabetical_caps)}{random.choice(alphabetical_caps)}{random.choice(numerical_digits)}{random.choice(numerical_digits)}_{dt.now(india_timezone).strftime('%d-%m')}"
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
    with open('orders_log.json', 'w', encoding = 'utf-8') as o2: #Add new order to Orders file
        json.dump(orderdata, o2, indent=2)
    print("New delivery order has been added to 'deliveries'.\nYour order should be delivered to you within 30 minutes.")
    return (f"Please kindly pay your bill during delivery.\n  Rs.{vtotal_price}\n  Bill ID: {bill_id}")


def br(): #Prints a line of equal signs
    print("="*70)


def home(clearv = True): #Home screen
    if clearv:
        clear()
    br()
    chosen_menu = ginput("Enter what you want to see: \n'o' : Order Food\n't' : Track Orders\n'm' : Show Menu\n'a' : Accounting\n'exit' : Exit Program\n" ,str,['o','m','t','a','exit'],True)
    clear()
    if chosen_menu == 'm':
        print_categorized_menu(menudata, False)
        home()
    elif chosen_menu == 'o':
        print_categorized_menu(menudata, True)
    elif chosen_menu == 't':
        tracking()
    elif chosen_menu == 'a':
        accounting()
    elif chosen_menu == 'exit':
        sys.exit()

def accounting():
    clear()
    br()
    is_admin = admin_access()
    if is_admin:
        br()
        sales = [order['price'] for order in orderdata['deliveries']]
        print(f"    Accounting:\n\n\
    Total Deliveries: {len(sales)}\n\
    Total Payment: Rs.{sum(sales)}\n\
    Estimated Expenses: Rs.{sum(sales)*62/100}\n\
    Estimated Profit (without GST): Rs.{sum(sales)*38/100}")
    else:
        print("You need admin access")
    br()
    input("Enter to go to home.")
    home()


def tracking(): #Track Existing and Current Order by its ID or show all Orders
    clear()
    br()
    all_orders = [order['order_id'] for order in orderdata['deliveries']]
    orders_and_more = all_orders+['last','recent']
    get_id = ginput("Enter your Order ID here: (Enter 'last' to see last made order or 'recent' to see last 10 orders):  ", str, orders_and_more, False)
    if get_id == 'last' or 'recent':
        is_admin = admin_access()
        if is_admin:
            if get_id == 'last':
                while True and len(all_orders) > 0:
                    for item_id in all_orders[-1:]:
                        br()
                        get_order_info(item_id)
                    br()
                    cont = ginput("Enter anything to see previous order or 'exit' to exit: ", str, [], True)
                    if cont == 'exit':
                        break
                    else:
                        all_orders.pop()
                        continue
            elif get_id == 'recent':
                while True and len(all_orders) > 10:
                    for item_id in all_orders[-10:]:
                        br()
                        get_order_info(item_id)
                    br()
                    cont = ginput("Enter anything to see previous 10 orders or 'exit' to exit: ", str, [], True)
                    if cont == 'exit':
                        break
                    else:
                        for _ in range(10):
                            all_orders.pop()
                        continue
        else:
            print("You need admin access")
    else:
        br()
        get_order_info(get_id)
    br()
    input("Enter to go to home.")
    home()


def get_order_info(order_id_input): #Find the order in deliveries and show its info by its ID
    index = next((i for i, delivery in enumerate(orderdata["deliveries"]) if delivery["order_id"] == order_id_input), None)
    ordered_by = orderdata['deliveries'][index]['name']
    order_value = orderdata['deliveries'][index]['price']
    ordered_items = [item['name'] for item in orderdata['deliveries'][index]['order_details']]
    order_time = orderdata['deliveries'][index]['time_of_order']
    order_address = orderdata['deliveries'][index]['address']
    print(f"Order ID: {order_id_input}\nOrdered By: {ordered_by}\nTotal price: {order_value}\nTime of Order: {order_time}\nOrdered Items:{ordered_items}\nAddress: {order_address}")


def main(): #Main
    home(clearv= False)


if __name__ == "__main__":
    br()
    print("Welcome to FlavourSync")
    main()