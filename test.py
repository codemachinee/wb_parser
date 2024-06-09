from datetime import *
import pytz
moscow_tz = pytz.timezone('Europe/Moscow')



value = str(datetime.now(moscow_tz).strftime('%d.%m.%y %H:%M'))
print(value)
print(value.split(' ')[0])
print(value.split(' ')[0] == str(datetime.now(moscow_tz).strftime('%d.%m.%y')))