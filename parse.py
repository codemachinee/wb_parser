import requests

cookies = {
    'external-locale': 'ru',
    '_wbauid': '5046956441695983060',
    'BasketUID': 'a1a0e8d6-934f-46d0-9fcd-aa6a69bc79b3',
    '__wba_s': '1',
    '___wbu': '52cc0a23-cfd0-4125-b777-1c2e953f5ab3.1695983060',
    '___wbs': '23ed9980-7b2f-4071-a11f-2ed4dc96832e.1695983060',
}

headers = {
    'authority': 'www.wildberries.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'external-locale=ru; _wbauid=5046956441695983060; BasketUID=a1a0e8d6-934f-46d0-9fcd-aa6a69bc79b3; __wba_s=1; ___wbu=52cc0a23-cfd0-4125-b777-1c2e953f5ab3.1695983060; ___wbs=23ed9980-7b2f-4071-a11f-2ed4dc96832e.1695983060',
    'dnt': '1',
    'if-modified-since': 'Thu, 28 Sep 2023 13:52:06 GMT',
    'referer': 'https://www.wildberries.ru/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.2271 YaBrowser/23.9.0.2271 Yowser/2.5 Safari/537.36',
}

response = requests.get('https://www.wildberries.ru/', cookies=cookies, headers=headers)