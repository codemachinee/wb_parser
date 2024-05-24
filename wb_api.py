import base64
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from passwords import *
from exel import *

headers = {"Authorization": regular_api_wb}


class parse_date:
    global headers

    def __init__(self):
        pass

    async def get_price(self):
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
    async def get_news(self):
        data = []
        try:
            with open('news.txt', 'r') as file:
                file_id = file.read()
                params = {
                    # "from": f'{date.today() - timedelta(1)}'
                    "fromID": f"{file_id[:4]}"
                }
            BASE_URL = 'http://suppliers-api.wildberries.ru/api/communications/v1/news'
            response = requests.get(BASE_URL, headers=headers, params=params)
            with open('news.txt', 'w') as file:
                if len(response.json()['data']) != 0:
                    for i in response.json()['data']:
                        data.append(f"<em>{i['date']}</em>\n<strong>{i['header']}</strong>\n\n"
                                    f"{BeautifulSoup(i['text'], 'html.parser').get_text()}")
                        if i == response.json()['data'][-1]:
                            file.write(f"{i['id']}")
                        else:
                            pass
                    return data
                else:
                    with open('news.txt', 'w') as file:
                        file.write(f"{file_id}")
                        return None
        except requests.exceptions.JSONDecodeError as e:
            with open('news.txt', 'w') as file:
                file.write(f"{file_id}")
                data.append(f'Исключение: {e}')
            return data

    # список складов
    async def get_wb_warehouses(self):
        try:
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
            await data_to_exel("tables/список складов wb.xlsx", exel_headers, data, headers_rus=None)
        except Exception as e:
            return e

    # мои склады
    async def get_my_warehouses(self):
        try:
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
            await data_to_exel("tables/список моих складов.xlsx", exel_headers, data, headers_rus=None)
        except Exception as e:
            return e

    # список товаров
    async def get_goods_list(self):
        try:
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
            await data_to_exel("tables/список товаров.xlsx", exel_headers, data, headers_rus=None)
        except Exception as e:
            return e

    # список поставок за все время
    async def get_supplies_list(self):
        try:
            BASE_URL = 'https://suppliers-api.wildberries.ru/api/v3/supplies'
            params = {
                "limit": "1000",
                "next": "0",
            }
            response = requests.get(BASE_URL, headers=headers, params=params)
            print(response.status_code)
            for i in response.json()['supplies']:
                print(i)
        except Exception as e:
            return e

    # список поставок на текущий момент
    async def get_supplier_list(self):
        try:
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
            await data_to_exel("tables/Отчет о поставках.xlsx", exel_headers, response.json(), exel_headers_rus)
        except Exception as e:
            return e

    # остатки товаров на складах на текущий момент
    async def get_stocks_list(self):
        try:
            BASE_URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
            params = {
                "dateFrom": f"{date.today()}",
            }
            response = requests.get(BASE_URL, headers=headers, params=params)
            print(response.status_code)
            for i in response.json():
                print(i)
        except Exception as e:
            return e

    async def reportDetailByPeriod(self):
        try:
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
        except Exception as e:
            return e

    # получение списка неотвеченных вопросов по товарам
    async def report_questions(self):
        try:
            BASE_URL = 'https://feedbacks-api.wildberries.ru/api/v1/questions/report'
            params = {
                "isAnswered": "false"
            }
            response = requests.get(BASE_URL, headers=headers, params=params)
            print(response.status_code)
            file_content = base64.b64decode(response.json()["data"]["file"])
            with open("tables/report_questions.xlsx", "wb") as f:
                f.write(file_content)
        except Exception as e:
            return e

    # получение списка необработанных отзывов по товарам
    async def report_feedbacks(self):
        try:
            BASE_URL = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/report'
            params = {
                "isAnswered": "false"
            }
            response = requests.get(BASE_URL, headers=headers, params=params)
            print(response.status_code)
            file_content = base64.b64decode(response.json()["data"]["file"])
            with open('tables/report_feedbacks.xlsx', "wb") as f:
                f.write(file_content)
        except Exception as e:
            return e

    # тарифы на коробы
    async def get_tariffs_box(self):
        try:
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
            await data_to_exel("tables/Тарифы на короб.xlsx", exel_headers,
                               response.json()['response']['data']['warehouseList'], exel_headers_rus)
        except Exception as e:
            return e

    # тарифы на монопалет
    async def get_tariffs_pallet(self):
        try:
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
            await data_to_exel("tables/Тарифы на монопалет.xlsx", exel_headers,
                               response.json()['response']['data']['warehouseList'], exel_headers_rus)
        except Exception as e:
            return e

    # тарифы на возвраты
    async def get_tariffs_returns(self):
        try:
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
            await data_to_exel("tables/Тарифы на возвраты.xlsx", exel_headers,
                               response.json()['response']['data']['warehouseList'], exel_headers_rus)
        except Exception as e:
            return e


# parse_date().get_tovar_card()
# parse_date().get_price()
# parse_date().get_news()
# asyncio.run(parse_date().get_wb_warehouses())
# parse_date().get_my_warehouses()
# parse_date().get_goods_list()
# parse_date().get_stocks_list()
# parse_date().get_supplier_list()
# parse_date().get_supplies_list()
# parse_date().reportDetailByPeriod()
# asyncio.run(parse_date().report_questions())
# parse_date().report_feedbacks()
# parse_date().get_tariffs_box()
# parse_date().get_tariffs_pallet()
# parse_date().get_tariffs_returns()


