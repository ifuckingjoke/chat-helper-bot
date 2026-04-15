# imports

from api import *
import asyncio
from gui import dp, bot as aiogram_bot, private_rt
from bot import bot as telethon_bot

# start bots

async def start_telethon():
    await telethon_bot.start(bot_token=BOT_TOKEN)
    await telethon_bot.run_until_disconnected()

async def start_aiogram():
    dp.include_router(private_rt)
    await dp.start_polling(aiogram_bot)

async def start():

    await asyncio.gather(
        start_telethon(),
        start_aiogram()
    )

# start

if __name__ == "__main__":
    asyncio.run(start())
