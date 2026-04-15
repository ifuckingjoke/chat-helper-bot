
# telegram devoloper: @ifuckingjoke

import random # рандом для чисел
from logs import log # оболочка для логирования
from captcha.image import ImageCaptcha # байтовое представление картинки для капчи


len_text = 6

def generate_text():

    captcha_numbers = []

    for _ in range(len_text):

        captcha_numbers.append(str(random.randint(0, 10)))

    captcha_text = "".join(captcha_numbers)
    log(f"Текст капчи: { captcha_text }")

    return captcha_text

class Captcha:
    def __init__(self):

        image = ImageCaptcha(width=280, height=90)

        self.captcha_text = generate_text()
        self.captcha_image = image.generate(self.captcha_text)
        self.captcha_image.name = "captha.png"