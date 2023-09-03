import json
import pytz
from datetime import datetime as dt
from tabulate import tabulate
from res_library import get_input as ginput

with open("res_menu.json", encoding = 'utf-8') as f1:
    data = json.load(f1)
    menu = json.dumps(data, indent=4)

menu_data = data['menu']
for item_data in menu_data:
    print(menu_data)
