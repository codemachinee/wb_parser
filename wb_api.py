import base64

import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from passwords import *
from exel import *

headers = {"Authorization": regular_api}


class parse_date:
    global headers

    def __init__(self):
        pass

    def get_price(self):
        BASE_URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
        response = requests.get(BASE_URL, headers=headers)
        print(response.status_code)
        for i in response.json():
            print(f'id товара: {i["nmId"]} , цена товара: {i["price"]}, скидка: {i["discount"]}, '
                  f'промокод: {i["promoCode"]}, цена с учетом скидки: {int(i["price"] * (1 - int(i["discount"]) / 100))}')

    # получение карточек товаров
    def get_tovar_card(self):
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
        BASE_URL = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        response = requests.post(BASE_URL, headers=headers, json=parametrs)
        print(response.status_code)
        for i in response.json()['data']['cards']:
            print(f"фото: {i['mediaFiles']}")

   # ежедневные новости
    def get_news(self):
        try:
            with open('news.txt', 'r') as file:
                file_id = file.read()
                params = {
                    # "from": f'{date.today() - timedelta(1)}'
                    "fromID": f"{file_id}"
                }
            BASE_URL = 'http://suppliers-api.wildberries.ru/api/communications/v1/news'
            response = requests.get(BASE_URL, headers=headers, params=params)
            data = ''
            print(response.status_code)
            with open('news.txt', 'w') as file:
                if len(response.json()['data']) != 0:
                    for i in response.json()['data']:
                        data += f"{i['date']}\n{i['id']}, {i['header']}\n{BeautifulSoup(i['text'], 'html.parser').get_text()}\n"
                        if i == response.json()['data'][-1]:
                            file.write(f"{i['id']}")
                        else:
                            pass
                    print(data)
                else:
                    with open('news.txt', 'w') as file:
                        file.write(f"{file_id}")
        except requests.exceptions.JSONDecodeError:
            print('Исключение: Превышена допустимая частота запроса (1 запрос в 10 мин.)')
            with open('news.txt', 'w') as file:
                file.write(f"{file_id}")

    # список складов
    def get_wb_warehouses(self):
        BASE_URL = 'https://suppliers-api.wildberries.ru/api/v3/offices'
        response = requests.get(BASE_URL, headers=headers)
        data = []
        exel_headers = ["id", "название", "адрес", "принимаемый тип товара",
                        "тип доставки, который принимает склад", "является Вашим складом"]
        print(response.status_code)
        for i in response.json():
            data.append({'id': f'{i["id"]}', 'название': f'{i["name"]}', 'адрес': f'{i["address"]}',
                         'принимаемый тип товара': f'{"обычный" if i["cargoType"] == 1 else "сверхгабаритный товар"}',
                         'тип доставки, который принимает склад':
                         f'{"доставка на склад Wildberries" if i["deliveryType"] == 1 else ("доставка силами продавца" if i["deliveryType"] == 2 else "доставка курьером WB")}',
                         'является Вашим складом': f'{"является" if i["selected"] is True else "не является"}'})
        data_to_exel("список складов wb.xlsx", exel_headers, data, headers_rus=None)

    # мои склады
    def get_my_warehouses(self):
        BASE_URL = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
        response = requests.get(BASE_URL, headers=headers)
        data = []
        exel_headers = ["id", "название", "ID склада WB", "принимаемый тип товара",
                        "тип доставки, который принимает склад"]
        print(response.status_code)
        for i in response.json():
            data.append({'id': f'{i["id"]}', 'название': f'{i["name"]}', 'ID склада WB': f'{i["officeId"]}',
                         'принимаемый тип товара': f'{"обычный" if i["cargoType"] == 1 else "сверхгабаритный товар"}',
                         'тип доставки, который принимает склад':
                             f'{"доставка на склад Wildberries" if i["deliveryType"] == 1 else ("доставка силами продавца" if i["deliveryType"] == 2 else "доставка курьером WB")}'})
        data_to_exel("список моих складов.xlsx", exel_headers, data, headers_rus=None)


    # список товаров
    def get_goods_list(self):
        BASE_URL = 'https://discounts-prices-api.wb.ru/api/v2/list/goods/filter'
        params = {
            "limit": "1000",
            "offset": "0",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        data = []
        exel_headers = [f"id номенклатуры", "код производителя", "id размера", "цена без скидки", "цена со скидкой",
                        "размер", "валюта", "скидка %", "своя цена для размеров"]
        for i in response.json()['data']['listGoods']:
            data.append({'id номенклатуры': f'{i["nmID"]}', 'код производителя': f'{i["vendorCode"]}',
                         'id размера': f'{i["sizes"][0]["sizeID"]}', 'цена без скидки': f'{i["sizes"][0]["price"]}',
                         'цена со скидкой': f'{i["sizes"][0]["discountedPrice"]}',
                         'размер': f'{i["sizes"][0]["techSizeName"]}', 'валюта': f'{i["currencyIsoCode4217"]}',
                         'скидка %': f'{i["discount"]}', 'своя цена для размеров': f'{i["editableSizePrice"]}'})
        data_to_exel("список товаров.xlsx", exel_headers, data, headers_rus=None)

    # список поставок за все время
    def get_supplies_list(self):
        BASE_URL = 'https://suppliers-api.wildberries.ru/api/v3/supplies'
        params = {
            "limit": "1000",
            "next": "0",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        for i in response.json()['supplies']:
            print(i)

    # список поставок на текущий момент
    def get_supplier_list(self):
        BASE_URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/incomes'
        params = {
            "dateFrom": f"{date.today()}",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        exel_headers_rus = ["Номер поставки", "Номер УПД", "Дата поступления", "Время обновления информации в сервисе",
                            "Артикул продавца", "Размер товара", "Бар-код", "Количество", "Цена из УПД",
                            "Дата принятия (закрытия) в WB", "Склад", "Артикул WB", "Статус поставки"]
        exel_headers = ["incomeId", "number", "date", "lastChangeDate", "supplierArticle", "techSize", "barcode",
                        "quantity", "totalPrice", "dateClose", "warehouseName", "nmId", "status"]
        data_to_exel("Отчет о поставках.xlsx", exel_headers, response.json(), exel_headers_rus)

    # остатки товаров на складах на текущий момент
    def get_stocks_list(self):
        BASE_URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
        params = {
            "dateFrom": f"{date.today()}",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        for i in response.json():
            print(i)

    def reportDetailByPeriod(self):
        BASE_URL = 'https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod'
        params = {
            "dateFrom": "2023-01-20",
            "dateTo": "2024-02-20",
            "rrdid": "0"
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        for i in response.json():
            print(i)

    # получение списка неотвеченных вопросов по товарам
    def report_questions(self):
        BASE_URL = 'https://feedbacks-api.wildberries.ru/api/v1/questions/report'
        params = {
            "isAnswered": "false"
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        file_content = base64.b64decode(response.json()["data"]["file"])
        with open("report_questions.xlsx", "wb") as f:
            f.write(file_content)

    # получение списка необработанных отзывов по товарам
    def report_feedbacks(self):
        BASE_URL = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/report'
        params = {
            "isAnswered": "false"
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        file_content = base64.b64decode(response.json()["data"]["file"])
        with open('report_feedbacks.xlsx', "wb") as f:
            f.write(file_content)

    # тарифы на коробы
    def get_tariffs_box(self):
        BASE_URL = 'https://common-api.wildberries.ru/api/v1/tariffs/box'
        params = {
            "date": f"{date.today()}",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        exel_headers = ['boxDeliveryAndStorageExpr', 'boxDeliveryBase', 'boxDeliveryLiter',	'boxStorageBase',
                        'boxStorageLiter',	'warehouseName']
        exel_headers_rus = ['boxDeliveryAndStorageExpr', 'boxDeliveryBase', 'boxDeliveryLiter',	'boxStorageBase',
                            'boxStorageLiter',	'склад']
        data_to_exel("Тарифы на короб.xlsx", exel_headers,
                     response.json()['response']['data']['warehouseList'], exel_headers_rus)

    # тарифы на монопалет
    def get_tariffs_pallet(self):
        BASE_URL = 'https://common-api.wildberries.ru/api/v1/tariffs/pallet'
        params = {
            "date": f"{date.today()}",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        exel_headers = ['palletDeliveryExpr', 'palletDeliveryValueBase', 'palletDeliveryValueLiter', 'palletStorageExpr',
                        'palletStorageValueExpr',	'warehouseName']
        exel_headers_rus = ['palletDeliveryExpr', 'palletDeliveryValueBase', 'palletDeliveryValueLiter',
                            'palletStorageExpr', 'palletStorageValueExpr',	'склад']
        data_to_exel("Тарифы на монопалет.xlsx", exel_headers,
                     response.json()['response']['data']['warehouseList'], exel_headers_rus)

    # тарифы на возвраты
    def get_tariffs_returns(self):
        BASE_URL = 'https://common-api.wildberries.ru/api/v1/tariffs/return'
        params = {
            "date": f"{date.today()}",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        print(response.status_code)
        exel_headers = ["deliveryDumpKgtOfficeBase", "deliveryDumpKgtOfficeLiter", "deliveryDumpKgtReturnExpr",
                        "deliveryDumpSrgOfficeExpr", "deliveryDumpSrgReturnExpr", "deliveryDumpSupCourierBase",
                        "deliveryDumpSupCourierLiter", "deliveryDumpSupOfficeBase", "deliveryDumpSupOfficeLiter",
                        "deliveryDumpSupReturnExpr", "warehouseName"]
        exel_headers_rus = ["deliveryDumpKgtOfficeBase", "deliveryDumpKgtOfficeLiter", "deliveryDumpKgtReturnExpr",
                            "deliveryDumpSrgOfficeExpr", "deliveryDumpSrgReturnExpr", "deliveryDumpSupCourierBase",
                            "deliveryDumpSupCourierLiter", "deliveryDumpSupOfficeBase", "deliveryDumpSupOfficeLiter",
                            "deliveryDumpSupReturnExpr", "склад"]
        data_to_exel("Тарифы на возвраты.xlsx", exel_headers,
                     response.json()['response']['data']['warehouseList'], exel_headers_rus)


# parse_date().get_tovar_card()
# parse_date().get_price()
parse_date().get_news()
# parse_date().get_wb_warehouses()
# parse_date().get_my_warehouses()
# parse_date().get_goods_list()
# parse_date().get_stocks_list()
# parse_date().get_supplier_list()
# parse_date().get_supplies_list()
# parse_date().reportDetailByPeriod()
# parse_date().report_questions()
# parse_date().report_feedbacks()
# parse_date().get_tariffs_box()
# parse_date().get_tariffs_pallet()
# parse_date().get_tariffs_returns()


