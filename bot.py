
# telegram devoloper: @ifuckingjoke

from api import * # api
from datetime import datetime # дата и время
import asyncio # модуль для ассинхроного программирование
from logs import log # оболочка для логирования
from state import BotState # общие состояния, память 
from telethon.sync import TelegramClient, events, utils # отслеживание действий в чате, утилиты telethon
from telethon.tl.types import PeerChannel, PeerUser # классы представления лс бота и чата
from captcha_challenge import Captcha # класс капчи

bot = TelegramClient("bot", API_ID, API_HASH)

wait_captcha = {}  # (user_id, chat_id) -> {"text": str, "captcha_msg_id": int, "attempts": int}

async def get_username(user):
    if user.username:
        username_text = "@" + user.username
    elif user.username is None:
        username_text = ""
    else:
        username_text = user.first_name
    
    return username_text

async def send_greeting(event, user):
    """Отправляет приветствие пользователю"""

    username_text = await get_username(user)

    greeting_list = BotState.greeting_text.copy()
    display_greeting = []
    
    for word in greeting_list:
        greeting_text = word.replace("[username]", username_text)
        display_greeting.append(greeting_text)

    await bot.send_message(event.chat_id, message=" ".join(display_greeting))
    log(f"{username_text} присоединился к чату {event.chat_id}")

@bot.on(events.ChatAction)
async def cmd_user_init(event):
    if event.user_joined:
        user = await event.get_user()
        log(f"{user.first_name} инициализирован в чате {event.chat_id}")

        if BotState.is_enable_captcha:
            captcha = Captcha()
            sent = await bot.send_file(
                event.chat_id,
                file=captcha.captcha_image,
                caption="🔐 Пройдите капчу (введите текст с картинки)"
            )
            wait_captcha[(user.id, event.chat_id)] = {
                "text": captcha.captcha_text,
                "captcha_msg_id": sent.id,
                "attempts": 0,
                "bot_msg_id": []
            }
        else:
            await send_greeting(event, user)
    if event.user_left:

        if BotState.is_enable_captcha:

            data = wait_captcha.get((event.user_id, event.chat_id))

            if data:
                if data.get("bot_msg_id"):
                    to_delete = [data["captcha_msg_id"], *data["bot_msg_id"]]
                    await bot.delete_messages(event.chat_id, to_delete)

                    wait_captcha.pop((event.user_id, event.chat_id), None)

                else:
                    await bot.delete_messages(event.chat_id, data["captcha_msg_id"]) 

                    wait_captcha.pop((event.user_id, event.chat_id), None)
            else:
                return   
        else:
            return


@bot.on(events.NewMessage)
async def new_message_captcha(event):

    if isinstance(event.message.peer_id, PeerChannel):
        data = wait_captcha.get((event.sender_id, event.chat_id))

        if not data:
            return  # не ждём капчу от этого пользователя

        # Успешная капча
        if event.text == data["text"]:
            user = await event.get_sender()
            await send_greeting(event, user)

            # Удаляем сообщение с капчей и ответ пользователя
            await bot.delete_messages(event.chat_id, [data["captcha_msg_id"], event.message.id] + data["bot_msg_id"])

            wait_captcha.pop((event.sender_id, event.chat_id), None)

        else:
        # Неверная капча
            data["attempts"] += 1
            await event.delete()  # удаляем неверное сообщение
            msg = await event.respond(f"❌ Неверно. Попыток: {data['attempts']}/3")
            data["bot_msg_id"].append(msg.id)


        if data["attempts"] >= 3:
            # Удаляем капчу и уведомления о неверном вводе
            await bot.delete_messages(event.chat_id, [data["captcha_msg_id"], event.message.id] + data["bot_msg_id"])
            # Кикаем пользователя
            await bot.kick_participant(event.chat_id, event.sender_id)
        
            wait_captcha.pop((event.sender_id, event.chat_id), None)
    else:
        return
    
@bot.on(events.NewMessage)
async def new_message(event):

    if isinstance(event.message.peer_id, PeerChannel):

        if not BotState.bw_list:
            return
        
        user = await event.get_sender()

        active_index = BotState.bw_active

        username_text = await get_username(user)
        
        if BotState.bw_active is not None:

            user_msg = event.message.text.lower()

            try:
                if BotState.bw_list[active_index]:
                        
                    if any(bad_word in user_msg for bad_word in BotState.bw_list[active_index]):

                        await bot.delete_messages(event.chat_id, event.message.id)

                        await bot.send_message(
                            event.chat_id,
                            message=f"⚠️ {username_text} вы использовали запрещённое слово!\n"
                        )

            except IndexError:
                return
    else:
        return

@bot.on(events.NewMessage(pattern="^/report$"))
async def cmd_report(event):
    
    if isinstance(event.message.peer_id, PeerChannel):

        time = datetime.now().strftime("%H:%M:%S")
        
        msg = await event.get_reply_message()

        if not msg:
            await bot.send_message(
                event.chat_id,
                message="⚠️ Отправьте команду в ответ на сообщение"
            )
            return

        chat = await event.get_chat()

        if len(BotState.reports_list) >= 5:
            BotState.reports_list.clear()

        if getattr(chat, "username", None):
            msg_link = f"https://t.me/{chat.username}/{msg.id}"
            text = f"[{time}] {msg_link}"
            BotState.reports_list.append(text)
            log("Новый репорт добавлен в reports_list. Тип чата: публичный")
            log(f"{BotState.reports_list}")

            await bot.send_message(
                ADMIN_ID,
                message=f"⚠️ Новый репорт!\n{text}\nПолный список жалоб - /reports"
            )

        else:
            chat_id = utils.get_peer_id(event.peer_id)
            clean_id = str(chat_id).replace("-100", "")
            msg_link = f"https://t.me/c/{clean_id}/{msg.id}"
            text = f"[{time}] {msg_link}"
            BotState.reports_list.append(text)
            log("Новый репорт добавлен в reports_list. Тип чата: приватный")
            log(f"{BotState.reports_list}")

            await bot.send_message(
                ADMIN_ID,
                message=f"⚠️ Новый репорт!\n{text}\nПолный список жалоб - /reports"
            )
        
        await event.reply(
            message="📢 Отчёт отправлен администраторам чата"
        )

    else:
        return