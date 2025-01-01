import json
from datetime import datetime, timedelta


def check_date():
    with open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for row in data[2:]:
        print(row)
        break


check_date()