from datetime import datetime

import pytz

moscow_tz = pytz.timezone('Europe/Moscow')

# Получение текущего времени в московской временной зоне
moscow_time = datetime.now(moscow_tz).strftime('%d.%m.%y %H:%M')

print(moscow_time)