# ChatHelper - Telegram chat bot

![Open Badge](https://img.shields.io/badge/OpenSource-❤️-pink)
![GitHub stars](https://img.shields.io/github/stars/ifuckingjoke/ChatHelper?style=social)
![Python Badge](https://img.shields.io/badge/Language-Python-blue)
![GitHub Tag](https://img.shields.io/badge/Realese-latest-green)

**🌐 Язык: [Русский](README.md) | 🌐 Language: [English](README-EN-US.md)**

___

**ChatHelper** - бот с открытым исходным кодом для модерации ваших чатов в telegram, а также защиты от ботов на стадии проникновения в чат.

## ⚙️ Основные функции

:clap: Взаимодействие с пользователями 
  + Возможность приветствовать новых пользователей в чате

:shield: Модерация в чатах
  + Возможность добавления запрещённых слов и предложений
  + Система репортов с уведомлениями в боте

:robot: Защита от ботов (визуальная капча)
+ Не позволяет писать пользователю в чат, пока он не пройдёт капчу
    + Удаляется и удаляет все неудачные попытки, если пользователь выходит из чата
    + Удаляется и удаляет все неудачные попытки, если пользователь не смог пройти её с 3-х попыток

:trollface: Полностью ваша система
  + Система моментальной авторизации владельца по telegram id
  + Возможность авторизации с помощью пароля в боте

## :arrow_down: Установка

> :warning: для дальнейших действий нужно получить **BOT_TOKEN** в официальном боте от telegram **@BotFather**, создав бота

### 1. Скачайте код с репозитория

```bash
git clone https://github.com/ifuckingjoke/ChatHelper
```

## 1.1 API Keys

Сначала нужно получить API_ID и API_HASH. Сделать это можно на сайте - https://my.telegram.org после создания приложения
  
После получения BOT_TOKEN, API_ID, API_HASH в директории бота нужно отредактировать файл api.py

```python

BOT_TOKEN = "" # ваш BOT_TOKEN
API_ID = ... # ваш API_ID
API_HASH = "" # ваш API_HASH

ADMIN_ID = ... # ваш telegram id

ADMIN_PASSWORD = "" # придумайте надёжный пароль

```

> Cвой telegram id можно узнать с помощью @userinfobot

## 2. Docker

Для дальнейшней установки понадобится Docker. Ознакомиться с ним можно здесь - https://docs.docker.com

1. В директории бота выполните:

```bash
docker build -t bot:latest .
```

2. После сборки выполните запуск:
```bash
docker run -d bot
```


## :rainbow: Логирование

Бот оставляет логи. Для их просмотра воспользуйтесь командой:
```bash
docker logs CONTAINER_ID 
```

Для просмотра логов в реальном времени:

```bash
docker logs -f CONTAINER_ID
```

Узнать CONTAINER_ID:
```bash
docker ps
```

## ⚖️ Лицензия

Используется лицензия MIT. Подробнее можно ознакомиться в файле лицензии - [MIT](LICENSE)

## 📕 Контакты 

Telegram devoloper - https://t.me/ifuckingjoke
