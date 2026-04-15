
# telegram devoloper: @ifuckingjoke

from logs import log # оболочка для логирования 

class BotState:

    greeting_text: list = ["Привет", "[username]!", "Как твои дела?"]
    is_enable_captcha: bool = False
    bw_list = []
    bw_index = None
    bw_active = None
    reports_list = []

    log(f"Приветственное сообщение: {greeting_text}")
    log(f"is_enable_captcha: {is_enable_captcha}")
    log(f"Список запрещённых слов: {bw_list}")
    log(f"bw_index: {bw_index}")
    log(f"Активный список запрещённых слов: {bw_active}")
    log(f"Список репортов: {reports_list}")
    
