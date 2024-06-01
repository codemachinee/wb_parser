import requests
from bs4 import BeautifulSoup
from passwords import *
headers = {"Authorization": regular_api_wb}


def get_news():
    data = []
    try:
        with open('news.txt', 'r') as file:
            file_id = file.read()
            params = {
                # "from": f'{date.today() - timedelta(1)}'
                "fromID": f"{file_id}"
            }
        BASE_URL = 'http://suppliers-api.wildberries.ru/api/communications/v1/news'
        response = requests.get(BASE_URL, headers=headers, params=params)
        with open('news.txt', 'w') as file:
            print(f'response.json():\n{response.json()}')
            print(f'response.json()["data"]:\n{response.json()["data"]}')
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
    except requests.exceptions.JSONDecodeError:
        with open('news.txt', 'w') as file:
            file.write(f"{file_id}")
            pass
            # data.append(f'Исключение: {e}')
        # return data


print(get_news())
