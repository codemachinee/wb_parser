import base64
import asyncio
import json

import aiofiles
import aiohttp
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
        base_url = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers) as response:
                    response.raise_for_status()
                    json_data = await response.json()
        # print(response.status_code)
                    for i in json_data:
                        print(f'id товара: {i["nmId"]} , цена товара: {i["price"]}, скидка: {i["discount"]}, '
                              f'промокод: {i["promoCode"]}, цена с учетом скидки: {int(i["price"] * (1 - int(i["discount"]) / 100))}')
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_price', e)
            return e

    # получение карточек товаров
    async def get_tovar_card(self):
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
        base_url = 'https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(base_url, headers=headers, json=parametrs) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    for i in json_data['data']['cards']:
                        print(f"фото: {i['mediaFiles']}")
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_tovar_card', e)
            return e

   # ежедневные новости
    async def get_news(self):
        data = []
        base_url = 'https://common-api.wildberries.ru/api/communications/v1/news'
        # try:
        async with aiofiles.open('news.txt', 'r') as file:
            file_id = await file.read()
            params = {
                # "from": f'{date.today() - timedelta(1)}'
                "fromID": f"{file_id}"
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, headers=headers, params=params) as response:
                response.raise_for_status()
                json_data = await response.json()
                async with aiofiles.open('news.txt', 'w') as file:
                    if len(json_data['data']) != 0:
                        for i in json_data['data']:
                            data.append(f"<em>{i['date']}</em>\n<strong>{i['header']}</strong>\n\n"
                                        f"{BeautifulSoup(i['text'], 'html.parser').get_text()}")
                            if i == json_data['data'][-1]:
                                await file.write(f"{int(i['id']+1)}")
                            else:
                                pass
                        # print(data)
                        return data
                    else:
                        await file.write(f"{file_id}")
                        return None
        # except requests.exceptions.JSONDecodeError as e:
        #     async with aiofiles.open('news.txt', 'w') as file:
        #         await file.write(f"{file_id}")
        #         pass
        #     logger.exception('Ошибка wb_api/send_news: JSONDecodeError', e)
            #     data.append(f'Исключение: {e}')
            # return data

    # список складов
    async def get_wb_warehouses(self):
        base_url = 'https://suppliers-api.wildberries.ru/api/v3/offices'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    data = []
                    exel_headers = ["id", "название", "адрес", "принимаемый тип товара",
                                    "тип доставки, который принимает склад", "является Вашим складом"]
                    # print(response.status_code)
                    for i in json_data:
                        data.append({'id': f'{i["id"]}', 'название': f'{i["name"]}', 'адрес': f'{i["address"]}',
                                     'принимаемый тип товара': f'{"обычный" if i["cargoType"] == 1 else "сверхгабаритный товар"}',
                                     'тип доставки, который принимает склад':
                                     f'{"доставка на склад Wildberries" if i["deliveryType"] == 1 else ("доставка силами продавца" if i["deliveryType"] == 2 else "доставка курьером WB")}',
                                     'является Вашим складом': f'{"является" if i["selected"] is True else "не является"}'})
                    await data_to_exel("tables/список складов wb.xlsx", exel_headers, data, headers_rus=None)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_wb_warehouses', e)
            return e

    # мои склады
    async def get_my_warehouses(self):
        base_url = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    data = []
                    exel_headers = ["id", "название", "ID склада WB", "принимаемый тип товара",
                                    "тип доставки, который принимает склад"]
                    # print(response.status_code)
                    for i in json_data:
                        data.append({'id': f'{i["id"]}', 'название': f'{i["name"]}', 'ID склада WB': f'{i["officeId"]}',
                                     'принимаемый тип товара': f'{"обычный" if i["cargoType"] == 1 else "сверхгабариnный товар"}',
                                     'тип доставки, который принимает склад':
                                         f'{"доставка на склад Wildberries" if i["deliveryType"] == 1 else ("доставка силами продавца" if i["deliveryType"] == 2 else "доставка курьером WB")}'})
                    await data_to_exel("tables/список моих складов.xlsx", exel_headers, data, headers_rus=None)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_my_warehouses', e)
            return e

    # список товаров
    async def get_goods_list(self):
        try:
            base_url = 'https://discounts-prices-api.wb.ru/api/v2/list/goods/filter'
            params = {
                "limit": "1000",
                "offset": "0",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    data = []
                    exel_headers = [f"id номенклатуры", "код производителя", "id размера", "цена без скидки", "цена со скидкой",
                                    "размер", "валюта", "скидка %", "своя цена для размеров"]
                    for i in json_data['data']['listGoods']:
                        data.append({'id номенклатуры': f'{i["nmID"]}', 'код производителя': f'{i["vendorCode"]}',
                                     'id размера': f'{i["sizes"][0]["sizeID"]}', 'цена без скидки': f'{i["sizes"][0]["price"]}',
                                     'цена со скидкой': f'{i["sizes"][0]["discountedPrice"]}',
                                     'размер': f'{i["sizes"][0]["techSizeName"]}', 'валюта': f'{i["currencyIsoCode4217"]}',
                                     'скидка %': f'{i["discount"]}', 'своя цена для размеров': f'{i["editableSizePrice"]}'})
                    await data_to_exel("tables/список товаров.xlsx", exel_headers, data, headers_rus=None)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_goods_list', e)
            return e

    # список поставок за все время
    async def get_supplies_list(self):
        try:
            base_url = 'https://suppliers-api.wildberries.ru/api/v3/supplies'
            params = {
                "limit": "1000",
                "next": "0",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    for i in json_data['supplies']:
                        print(i)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_supplies_list', e)
            return e

    # список поставок на текущий момент
    async def get_supplier_list(self):
        try:
            base_url = 'https://statistics-api.wildberries.ru/api/v1/supplier/incomes'
            params = {
                "dateFrom": f"{date.today()}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    exel_headers_rus = ["Номер поставки", "Номер УПД", "Дата поступления", "Время обновления информации в сервисе",
                                        "Артикул продавца", "Размер товара", "Бар-код", "Количество", "Цена из УПД",
                                        "Дата принятия (закрытия) в WB", "Склад", "Артикул WB", "Статус поставки"]
                    exel_headers = ["incomeId", "number", "date", "lastChangeDate", "supplierArticle", "techSize", "barcode",
                                    "quantity", "totalPrice", "dateClose", "warehouseName", "nmId", "status"]
                    await data_to_exel("tables/Отчет о поставках.xlsx", exel_headers, json_data, exel_headers_rus)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_supplier_list', e)
            return e

    # остатки товаров на складах на текущий момент
    async def get_stocks_list(self):
        try:
            base_url = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
            params = {
                "dateFrom": f"{date.today()}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    for i in json_data:
                        print(i)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_stocks_list', e)
            return e

    async def reportDetailByPeriod(self):
        try:
            base_url = 'https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod'
            params = {
                "dateFrom": "2023-01-20",
                "dateTo": "2024-02-20",
                "rrdid": "0"
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    for i in json_data:
                        print(i)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/reportDetailByPeriod', e)
            return e

    # получение списка неотвеченных вопросов по товарам
    async def report_questions(self):
        try:
            base_url = 'https://feedbacks-api.wildberries.ru/api/v1/questions/report'
            params = {
                "isAnswered": "false"
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    file_content = base64.b64decode(json_data["data"]["file"])
                    async with aiofiles.open("tables/report_questions.xlsx", "wb") as f:
                        await f.write(file_content)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/report_questions', e)
            return e

    # получение списка необработанных отзывов по товарам
    async def report_feedbacks(self):
        try:
            base_url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/report'
            params = {
                "isAnswered": "false"
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    file_content = base64.b64decode(json_data["data"]["file"])
                    async with aiofiles.open('tables/report_feedbacks.xlsx', mode="wb") as f:
                        await f.write(file_content)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/report_feedbacks', e)
            return e

    # тарифы на коробы
    async def get_tariffs_box(self):
        try:
            base_url = 'https://common-api.wildberries.ru/api/v1/tariffs/box'
            params = {
                "date": f"{date.today()}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    exel_headers = ['boxDeliveryAndStorageExpr', 'boxDeliveryBase', 'boxDeliveryLiter',	'boxStorageBase',
                                    'boxStorageLiter',	'warehouseName']
                    exel_headers_rus = ['boxDeliveryAndStorageExpr', 'boxDeliveryBase', 'boxDeliveryLiter',	'boxStorageBase',
                                        'boxStorageLiter',	'склад']
                    await data_to_exel("tables/Тарифы на короб.xlsx", exel_headers,
                                       json_data['response']['data']['warehouseList'], exel_headers_rus)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_tariffs_box', e)
            return e

    # тарифы на монопалет
    async def get_tariffs_pallet(self):
        try:
            base_url = 'https://common-api.wildberries.ru/api/v1/tariffs/pallet'
            params = {
                "date": f"{date.today()}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    exel_headers = ['palletDeliveryExpr', 'palletDeliveryValueBase', 'palletDeliveryValueLiter', 'palletStorageExpr',
                                    'palletStorageValueExpr',	'warehouseName']
                    exel_headers_rus = ['palletDeliveryExpr', 'palletDeliveryValueBase', 'palletDeliveryValueLiter',
                                        'palletStorageExpr', 'palletStorageValueExpr',	'склад']
                    await data_to_exel("tables/Тарифы на монопалет.xlsx", exel_headers,
                                       json_data['response']['data']['warehouseList'], exel_headers_rus)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_tariffs_pallet', e)
            return e

    # тарифы на возвраты
    async def get_tariffs_returns(self):
        try:
            base_url = 'https://common-api.wildberries.ru/api/v1/tariffs/return'
            params = {
                "date": f"{date.today()}",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    exel_headers = ["deliveryDumpKgtOfficeBase", "deliveryDumpKgtOfficeLiter", "deliveryDumpKgtReturnExpr",
                                    "deliveryDumpSrgOfficeExpr", "deliveryDumpSrgReturnExpr", "deliveryDumpSupCourierBase",
                                    "deliveryDumpSupCourierLiter", "deliveryDumpSupOfficeBase", "deliveryDumpSupOfficeLiter",
                                    "deliveryDumpSupReturnExpr", "warehouseName"]
                    exel_headers_rus = ["deliveryDumpKgtOfficeBase", "deliveryDumpKgtOfficeLiter", "deliveryDumpKgtReturnExpr",
                                        "deliveryDumpSrgOfficeExpr", "deliveryDumpSrgReturnExpr", "deliveryDumpSupCourierBase",
                                        "deliveryDumpSupCourierLiter", "deliveryDumpSupOfficeBase", "deliveryDumpSupOfficeLiter",
                                        "deliveryDumpSupReturnExpr", "склад"]
                    await data_to_exel("tables/Тарифы на возвраты.xlsx", exel_headers,
                                       json_data['response']['data']['warehouseList'], exel_headers_rus)
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_tariffs_returns', e)
            return e

    async def get_coeffs_warehouses(self):
        try:
            base_url = 'https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients'
            params = {
                "warehouseIDs": []
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, headers=headers, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    # print(response.status_code)
                    async with aiofiles.open('coeffs_from_api.json', 'w', encoding='utf-8') as file:
                        await file.write(json.dumps(json_data, indent=4, ensure_ascii=False))  # Сохранение в JSON файл
                    # print(f"Данные сохранены в файл {'coeffs_from_api.json'}")
                    return True
        except Exception as e:
            logger.exception(f'Ошибка wb_api/get_coeffs_warehouses', e)
            return e


# parse_date().get_tovar_card()
# parse_date().get_price()
# asyncio.run(parse_date().get_coeffs_warehouses())
# asyncio.run(parse_date().get_news())
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


