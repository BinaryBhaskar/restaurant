import json
import datetime as dt
import random
import string
import pytz

india_timezone = pytz.timezone('Asia/Kolkata')


def gen(n):
    with open('orders_log.json', 'r', encoding = 'utf-8') as o1: #Open Orders file
        orderdata = json.load(o1)

    with open("res_menu.json", encoding = 'utf-8') as f1: #Open Menu file
        menu_data = json.load(f1)
        menu = json.dumps(menu_data, indent=4)

    codeslist = [item['code'] for item in menu_data["menu"]]

    random_names = ['Alice', 'Bob', 'Charlie', 'David', 'Emma', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack', 'Katherine', 'Leo', 'Mia', 'Nathan', 'Olivia', 'Peter', 'Quinn', 'Rachel', 'Samuel', 'Tessa', 'Ulysses', 'Victoria', 'William', 'Xander', 'Yasmine', 'Zachary', 'Aria', 'Benjamin', 'Cora', 'Dylan', 'Eva', 'Finn', 'Giselle', 'Harrison', 'Isabella', 'Jacob', 'Kylie', 'Liam', 'Madison', 'Noah', 'Olivia', 'Peyton', 'Quincy', 'Riley', 'Sophia', 'Thomas', 'Uma']

    start_date = dt.datetime(2022, 1, 1)
    end_date = dt.datetime(2023, 9 , 9)
    alphabetical_caps = list(string.ascii_uppercase)
    numerical_digits = [str(i) for i in range(10)]
                    
    places = ['Maple Street', 'Meadow Lane', 'Oak Avenue', 'Sunnydale', 'Greenwood Terrace', 'Pine Street', 'Lakeview Drive', 'Rosewood Lane', 'Hillcrest Road', 'Cedar Lane', 'Highland Avenue', 'Riverbend Place', 'Willow Street', 'Magnolia Way', 'Sunset Boulevard', 'Brookside Drive', 'Riverside Avenue', 'Forest Hills', 'Valley View', 'Winding Road', 'Lakeside Avenue', 'Holly Court', 'Grove Street', 'Cypress Lane', 'Mountain View', 'Birch Avenue', 'Meadowbrook Lane', 'Sycamore Lane', 'Wildwood Avenue', 'Hawthorn Place', 'Amber Street', 'Whispering Pines', 'Golden Gate', 'Lighthouse Lane', 'Silkwood Way', 'Pebble Beach', 'Harbor View', 'Cherry Blossom Lane', 'Tranquil Terrace', 'Bluebell Lane', 'Prairie View', 'Eagle Ridge', 'Ivy Court', 'Ocean Drive', 'Royal Gardens', 'Silver Springs']

    countries = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France', 'Italy', 'Japan', 'Brazil', 'India', 'Spain', 'China', 'Mexico', 'South Africa', 'Russia', 'Argentina', 'Sweden', 'Netherlands', 'Switzerland', 'Singapore', 'New Zealand', 'Norway', 'Denmark', 'Finland', 'Ireland', 'Belgium', 'Portugal', 'Austria', 'Greece', 'South Korea', 'Turkey', 'India', 'Chile', 'Colombia', 'Egypt', 'Thailand', 'Vietnam', 'Malaysia', 'Indonesia', 'Philippines', 'Saudi Arabia', 'United Arab Emirates', 'Qatar', 'Kuwait', 'Oman', 'Bahrain', 'Jordan']

    for _ in range(n):

        random_date = start_date + dt.timedelta(days=random.randint(0, (end_date - start_date).days))
        random_time = dt.timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        random_datetime = random_date + random_time
        formatted_random_datetime = random_datetime.strftime('%d/%m/%Y, %A, %H:%M')
        ordered_list = []
        for _ in range(random.randint(1,4)):
            ordered_list.append(random.choice(codeslist))

        all_orders = [order['order_id'] for order in orderdata['deliveries']]
        while True:
            bill_id = f"{random.choice(alphabetical_caps)}{random.choice(alphabetical_caps)}{random.choice(numerical_digits)}{random.choice(numerical_digits)}_{random_datetime.strftime('%d-%m')}"
            if bill_id not in all_orders:
                break

        total_price = 0
        order_details = []
        for code in ordered_list:
            for item in menu_data["menu"]:
                if item['code'] == code:
                    total_price += item['price']
                    order_details.append(item)

        new_delivery_order = {
        "name": random.choice(random_names),
        "order_id": bill_id,
        "price": total_price,
        "order_details": order_details,
        "address": f"{random.randint(1,99)}, {random.choice(places)}, {random.choice(countries)}",
        "time_of_order": f"{formatted_random_datetime}"
        }

        orderdata["deliveries"].append(new_delivery_order)
        with open('orders_log.json', 'w', encoding = 'utf-8') as o2: #Add new order to Orders file
            json.dump(orderdata, o2, indent=2)

x = int(input("How many orders to generate randomly: "))
gen(x)
