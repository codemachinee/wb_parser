data = [
    {'nmID': 169378399, 'vendorCode': 'Говядина 5 кг', 'sizes': [{'sizeID': 281430437, 'price': 7200, 'discountedPrice': 1800, 'techSizeName': '0'}], 'currencyIsoCode4217': 'RUB', 'discount': 75, 'editableSizePrice': False}, 
    {'nmID': 169535021, 'vendorCode': 'Индейка 5 кг', 'sizes': [{'sizeID': 281677976, 'price': 7100, 'discountedPrice': 1775, 'techSizeName': '0'}], 'currencyIsoCode4217': 'RUB', 'discount': 75, 'editableSizePrice': False}
]

# Создаем заголовки столбцов на основе ключей первого словаря
headers = list(data[0].keys())
print(headers)