import requests
from passwords import *

headers = {"Authorization": regular_api}


parametrs = {
          "sort": {
              "cursor": {
                  "limit": 1000
              },
              "filter": {
                  "withPhoto": -1
              },
              "sortColumn": "",
              "ascending": 'false'
          }
        }


class parse_date:
    global headers
    global parametrs

    def __init__(self):
        pass

    def get_price(self):
        BASE_URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
        response = requests.get(BASE_URL, headers=headers)
        print(response.status_code)
        for i in response.json():
            print(f'id товара: {i["nmId"]} , цена товара: {i["price"]}, скидка: {i["discount"]}, '
                  f'промокод: {i["promoCode"]}, цена с учетом скидки: {int(i["price"] * (1 - int(i["discount"]) / 100))}')

    def get_tovar_card(self):
        BASE_URL = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        response = requests.post(BASE_URL, headers=headers, json=parametrs)
        print(response.status_code)
        for i in response.json()['data']['cards']:
            print(f"фото: {i['mediaFiles']}")


parse_date().get_tovar_card()


