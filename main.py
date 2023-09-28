import requests
from passwords import *
# BASE_URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
BASE_URL = 'https://suppliers-api.wildberries.ru/content/v1/object/all'
headers = {'Authorization': regular_api
           }

parametrs = {'name': 'корм'}

r = requests.get(BASE_URL, headers=headers, params=parametrs)
response = r
# print(response.status_code)
print(response.json())
