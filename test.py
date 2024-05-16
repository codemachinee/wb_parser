import math


def send_news():
    message = ['await parse_date().get_news()aasffsdfsd', 'await parse_date().get_news()aasffsdfsd']
    if message is None:
        pass
    else:
        for i in message:
            for n in range(0, math.ceil(len(i) / 10)):
                if n == (math.ceil(len(i) / 10) - 1):
                    print(f'{i[n*10:]}')

                else:
                    print(f'{i[n * 10:(n + 1) * 10]}')



send_news()