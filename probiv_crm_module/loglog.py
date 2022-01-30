#logging module
from datetime import datetime
import os

def get_current_time():
    now = datetime.now()
    dt = now.strftime("%d.%m.%Y %Hn%Mn%S")
    return dt


def logging(message):
    try: os.mkdir('logs')
    except Exception as e: pass

    timestamp = get_current_time().strip()
    with open(f'logs//{timestamp}_log.txt', 'w') as log_txt:
        log_txt.write(f'{message}\n')