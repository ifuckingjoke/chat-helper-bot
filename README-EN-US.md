# ChatHelper - Telegram chat bot

![Open Badge](https://img.shields.io/badge/OpenSource-❤️-pink)
![GitHub stars](https://img.shields.io/github/stars/ifuckingjoke/lis-byer?style=social)
![Python Badge](https://img.shields.io/badge/Language-Python-blue)
![GitHub Tag](https://img.shields.io/badge/Realese-latest-green)

**🌐 Language: [Russian](README.md) | 🌐 Language: [English](README-EN-US.md)**

___

**ChatHelper** - an open-source bot for moderating your Telegram chats, as well as protecting against bots at the stage of entering the chat.

## ⚙️ Main Features

:clap: User interaction  
  + Ability to welcome new users in the chat

:shield: Chat moderation  
  + Ability to add forbidden words and phrases  
  + Report system with notifications in the bot

:robot: Bot protection (visual captcha)  
+ Prevents users from sending messages until they pass the captcha  
    + Deleted along with all failed attempts if the user leaves the chat  
    + Deleted along with all failed attempts if the user fails it after 3 tries  

:trollface: Fully your system  
  + Instant owner authorization system via Telegram ID  
  + Ability to authorize using a password in the bot  

## :arrow_down: Installation

> :warning: for the following steps you need to get a **BOT_TOKEN** in the official Telegram bot **@BotFather** by creating a bot

### 1. Download the repository

```bash
git clone https://github.com/ifuckingjoke/ChatHelper
```

## 1.1 API Keys

First, you need to obtain API_ID and API_HASH. You can do this at https://my.telegram.org after creating an application

After getting BOT_TOKEN, API_ID, API_HASH, edit the api.py file in the bot directory

```python

BOT_TOKEN = "" # your BOT_TOKEN
API_ID = ... # your API_ID
API_HASH = "" # your API_HASH

ADMIN_ID = ... # your telegram id

ADMIN_PASSWORD = "" # create a strong password

```

> You can find your Telegram ID using @userinfobot

## 2. Docker

For further installation you will need Docker. You can learn more here - https://docs.docker.com

1. In the bot directory run:

```bash
docker build -t bot:latest .
```

2. After building, run:
```bash
docker run -d bot
```

## :rainbow: Logging

The bot keeps logs. To view them use:
```bash
docker logs CONTAINER_ID 
```

To view logs in real time:

```bash
docker logs -f CONTAINER_ID
```

Find CONTAINER_ID:
```bash
docker ps
```

## ⚖️ License

MIT License is used. You can learn more in the license file - [MIT](LICENSE)

## 📕 Contacts 

Telegram developer - https://t.me/ifuckingjoke
