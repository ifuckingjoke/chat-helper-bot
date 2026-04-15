
# telegram devoloper: @ifuckingjoke

from datetime import datetime # дата и время
from trgb import red, rgb # цвета для текста
import inspect # отслеживание фреймов
import os # работа с системой для получения названия файлов

last_filename = None

def title():

    global last_filename

    frame = inspect.currentframe().f_back.f_back
    filename = os.path.basename(frame.f_code.co_filename)

    if last_filename == filename:
        return
    else:

        last_filename = filename

        if filename == "gui.py":
            print(red("-------------------- GUI -----------------"))
        elif filename == "state.py":
            print(red("---------------------- StateBot ------------"))
        elif filename == "bot.py":
            print(red("---------------------- BOT ------------"))
        elif filename == "captcha_challenge.py":
            print(red("---------------------- Captcha ------------"))


def log(text):

    title()

    time = datetime.now().strftime("%H:%M:%S")
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_code.co_filename)
    line = frame.f_lineno

    print(rgb(199,21,133)(f"[ { time } ] [ {filename}:{line} ] {text}"))