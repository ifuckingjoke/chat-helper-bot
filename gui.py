# telegram devoloper: @ifuckingjoke

import asyncio #  модуль для ассинхроного програмирования: создание корутин, запуск, работа с фреймворками
from logs import log # специальная оболочка для логирования: файл logs.py
from state import BotState # общая память и состояния бота 
from aiogram import Dispatcher, Bot, F, Router # обработка команд, базовый класс для бота и F фильтр 
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, CallbackQuery
# сообщения, текстовая и инлайн клавиатуры, инлайн-кнопки, обработка callback_data 
from aiogram.filters import Command, StateFilter, or_f
# базовое обозначение команд, фильтр состояния, функция для логического or
from aiogram.fsm.context import FSMContext # обработка состояния
from aiogram.fsm.state import State, StatesGroup # базовые классы состояния
from aiogram.fsm.storage.memory import MemoryStorage # сохранения состояний в память
from aiogram.utils.keyboard import InlineKeyboardBuilder # Базовый класс для создания инлайн-клавиатур
from aiogram.utils.markdown import markdown_decoration as md # функции стиля разметки MD2
from aiogram.enums import ParseMode # подключение разметки в сообщения


from api import * # api

markup_list = [
   [KeyboardButton(text="👋 Приветствие")],
   [KeyboardButton(text="🤖 Капча")], 
   [KeyboardButton(text="🔞 Цензура")],
   [KeyboardButton(text="📢 Репорты")]
] 


markup = ReplyKeyboardMarkup(keyboard=markup_list, resize_keyboard=True, one_time_keyboard=True)

def get_captcha_keyboard():

   build_kb = InlineKeyboardBuilder() 

   text = "❌ Выключить" if BotState.is_enable_captcha else "✅ Включить" 

   build_kb.add(InlineKeyboardButton(text=text, callback_data="toggle_cptch")) 

   return build_kb.as_markup()

def get_greeting_keyboard():


   build_kb = InlineKeyboardBuilder() 

   text = "➕ Изменить приветствие"

   build_kb.add(InlineKeyboardButton(text=text, callback_data="edit_grt"))

   return build_kb.as_markup() 

def get_bw_keyboard():


   build_kb = InlineKeyboardBuilder()

   text = "➕ Добавить список" 

   build_kb.add(InlineKeyboardButton(text=text, callback_data="add_bwlist"))


   for bw_number, item in enumerate(BotState.bw_list, start=1): 

      if BotState.bw_active == bw_number - 1:

         build_kb.add(InlineKeyboardButton(text=f"✅ Список #{bw_number}", callback_data=f"bw_list_{bw_number}"))
      else:
         build_kb.add(InlineKeyboardButton(text=f"Список #{bw_number}", callback_data=f"bw_list_{bw_number}"))
      

      build_kb.adjust(1)

   return build_kb.as_markup() 

def set_bw_keyboard():

   build_kb = InlineKeyboardBuilder()

   text = ["➕ Использовать", "🗑️ Удалить"] 

   build_kb.add(
      InlineKeyboardButton(text=text[0], callback_data="set_bwl"), 
      InlineKeyboardButton(text=text[1], callback_data="rm_bwl")
      ) 

   build_kb.adjust(1) 
   
   return build_kb.as_markup() 

class States(StatesGroup):

   waiting_password = State()
   authorized = State() 
   waiting_new_greeting = State()
   waiting_bw_list = State() 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

private_rt = Router() 
private_rt.message.filter(StateFilter(States.authorized)) 


@private_rt.callback_query(F.data == "toggle_cptch")
async def captcha_toggle(callback: CallbackQuery):

   BotState.is_enable_captcha = not BotState.is_enable_captcha

   await callback.message.edit_reply_markup(reply_markup=get_captcha_keyboard())

   status = "✅ Капча была включена" if BotState.is_enable_captcha else "❌ Капча была выключена" 

   await callback.answer(show_alert=False)
   await callback.message.answer(
      f"{ status }",
      reply_markup=markup
   ) 

   log(f"значение is_enable_captcha было изменено: { BotState.is_enable_captcha }") 

@private_rt.callback_query(F.data == "edit_grt")
async def edit_greeting(callback: CallbackQuery, state: FSMContext):

   log("Ожидается ввод нового приветствия...") 

   help_text = (
   
      f">**{md.quote('Пользователь, присоединившийся в ваш чат, будет видеть текст, который вы напишите следующим сообщением')}\n\n"
      f">**{md.quote('[username] будет заменено на username пользователя, если он у него есть, иначе будет отобржаться его имя')}\n\n"
      f">**{md.quote('Пример: Привет [username]! Как твои дела? >> Привет @user! Как твои дела?')}"
   )

   await callback.answer(show_alert=False) 
   await callback.message.reply(
      "💬 Напишите новое приветствие\n\n"
      "❓ Как это работает\\?\n\n"
      + help_text,
      parse_mode = ParseMode.MARKDOWN_V2
   )

   await state.set_state(States.waiting_new_greeting)
   log("Смена состояния: waiting_new_greeting")

@private_rt.callback_query(F.data == "add_bwlist") 
async def add_bwlist(callback: CallbackQuery, state: FSMContext):
   
   log("Ожидается новый список...")

   await callback.answer(show_alert=False)
   await callback.message.reply(
      "Напишите новый список плохих слов..."
   )

   await state.set_state(States.waiting_bw_list)
   log("Смена состояния: waiting_bw_list")

@private_rt.callback_query(F.data.startswith("bw_list_"))
async def choice_bw_list(callback: CallbackQuery):

   list_number = int(callback.data.split('_')[-1])
   index = list_number - 1

   keyboard = set_bw_keyboard()

   if 0 <= index < len(BotState.bw_list):

      BotState.bw_index = index

      await callback.answer(show_alert=False)
      await callback.message.answer(
         f"📋 Список запрещённых слов #{list_number}\n\n"
         "⁉️ Cодержание:\n\n"
         f"🤬{','.join(BotState.bw_list[index])}🤬",
         reply_markup=keyboard
      )

@private_rt.callback_query(F.data == "set_bwl")
async def set_bwlist(callback: CallbackQuery):
   
   BotState.bw_active = BotState.bw_index

   await callback.answer(show_alert=False)
   await callback.message.answer(
      "✅ Список используется",
      reply_markup=markup
   )

   log(f"Выбран список с index[{BotState.bw_active}]")

@private_rt.callback_query(F.data == "rm_bwl")
async def rm_bwlist(callback: CallbackQuery):

   rm_index = BotState.bw_index

   BotState.bw_list.pop(rm_index)

   await callback.answer(show_alert=False)
   await callback.message.answer(
      "✅ Список успешно удалён",
      reply_markup=markup
   )

   log(f"Список index[{rm_index}] был удалён")
   

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
   log("Обработка команды 'start'")
   if message.from_user.id == ADMIN_ID:
      log("Индентификация пройдена: Owner")
      await message.answer(
         f"👋 { message.from_user.full_name }, добро пожаловать в ChatHelper!",
         reply_markup=markup
      )
      await state.set_state(States.authorized)
   else:
      await message.answer(
         "🔒 Функционал заблокирован. Введите пароль:"
      )

      await state.set_state(States.waiting_password)
      log("Смена состояния: waiting_password")

@dp.message(StateFilter(States.waiting_password))
async def process_password(message: Message, state: FSMContext):
   if message.text == ADMIN_PASSWORD:
      log("Индентификация пройдена: Admin")
      log("Клавиатура создана")
      await message.answer(
         "🔓 Функционал разблокирован. Добро пожаловать в ChatHelper!",
         reply_markup=markup
      )
      await state.set_state(States.authorized)
      log("Смена состояния: authorized")
   else:
      log("Неудачная попытка входа с помощью пароля")
      await message.answer("❌")

@dp.message(StateFilter(States.waiting_new_greeting))
async def process_new_greeting(message: Message, state: FSMContext):

   new_greeting = message.text 

   BotState.greeting_text = new_greeting.split(" ")

   await message.reply(
      "✅ Приветственное сообщение изменено",
      reply_markup=markup
      )

   log("Приветсветнное сообщение изменено для всех чатов")

   await state.set_state(States.authorized)
   log("Смена состояния: authorized")

@dp.message(StateFilter(States.waiting_bw_list))
async def process_new_bw_list(message: Message, state: FSMContext):

   text = message.text.lower()

   new_list = [ word.strip() for word in text.split(",")]

   BotState.bw_list.append(new_list)

   log(f"Новый список плохих слов: {BotState.bw_list}")

   await message.reply(
      "✅ Новый список сохранён\n\n"
      "❓ Вы можете посмотреть этот и другие ваши списки с помощью команды - /censure",
      reply_markup=markup
   )

   await state.set_state(States.authorized)
   log("Смена состояния: authorized")

@private_rt.message(or_f(Command("captcha"), F.text == "🤖 Капча"))
async def cmd_captcha(message: Message):
   log("Обработка команды 'captcha'")

   keyboard = get_captcha_keyboard()
   
   await message.reply(
      "Капча",
      reply_markup=keyboard
      )

@private_rt.message(or_f(Command("greeting"), F.text == "👋 Приветствие"))
async def cmd_greeting(message: Message):
   log("Обработка команды 'greeting'")

   keyboard = get_greeting_keyboard()

   await message.answer(
      "Изменить приветствие",
      reply_markup=keyboard
   )

@private_rt.message(or_f(Command("censure"), F.text == "🔞 Цензура"))
async def cmd_censure(message: Message):
   log("Обработка команды 'censure'")

   keyboard = get_bw_keyboard()

   await message.answer(
      "списки запрещённых слов:",
      reply_markup=keyboard
   )

@private_rt.message(or_f(Command("reports"), F.text == "📢 Репорты"))
async def cmd_reposts(message: Message):
   log("Обработка команды 'reports'")

   help_text = (

            f"**>{md.quote('Команда /report, использованная пользователем в чате отправляет уведомление вам в бот с ссылкой на нарушающее сообщение.')}\n"
            f"**>{md.quote('Как только вам придёт хотя-бы один репорт, он появится здесь.')}\n"
            f"**>{md.quote('После пяти репортов запись начинается сначала.')}\n"
      )

   if len(BotState.reports_list) < 1:

      await message.answer(
         "📢 В данный момент нет ни одного репорта\n\n"
         "⁉️ Как это работает\\?\n\n"
         + help_text,
         reply_markup=markup,
         parse_mode=ParseMode.MARKDOWN_V2
      )
   else:
      reports = "\n".join(BotState.reports_list)

      await message.answer(
         "📢 Последние репорты: \n\n"
         f"{reports}",
         reply_markup=markup
   )