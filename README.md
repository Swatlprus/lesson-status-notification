# Уведомление о проверке работа в Devman
Данный скрипт отправляет уведомление в Telegram, если преподаватель проверил урок у ученика.

## Подготовка к запуску
Для запуска сайта вам понадобится Python 3.8+ версии. 

Чтобы скачать код с Github, используйте команду:
```shell
git clone https://github.com/Swatlprus/lesson-status-notification.git
```
Для создания виртуального окружения используйте команду (Linux):
```shell
python3 -m venv venv
```
Для установки зависимостей, используйте команду:
```shell
pip3 install -r requirements.txt
```

## Настройка переменных окружения
Пример .env файла
```
DVMN_TOKEN=Token 5e97a8f265e4bfdb
TELEGRAM_TOKEN=65520:AAExux2WuW-GnfEzvAxEgan0g7o
TG_CHAT_ID=316445592
```
DVMN_TOKEN - Токен ключ от сайт Devman. Смотреть здесь - https://dvmn.org/api/docs/
TELEGRAM_TOKEN - Токен от Telegram бота. Создать его можно через https://t.me/BotFather
TG_CHAT_ID - Уникальный ID чата. Узнать свой можно с помощью бота - https://t.me/userinfobot

## Как запустить
Команда для запуска проекта локально (Linux):
```shell
python3 api.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).