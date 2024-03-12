import datetime

def fecha_y_hora(message):
    return datetime.datetime.fromtimestamp(message.date, datetime.timezone(datetime.timedelta(hours=1)))