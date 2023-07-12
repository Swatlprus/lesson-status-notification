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
RESERVE_TELEGRAM_TOKEN=33110:AAExux2fdsfdsWuW-Gfdsfdsn0g7o
TG_CHAT_ID=316445592
```
DVMN_TOKEN - Токен ключ от сайт Devman. Смотреть здесь - https://dvmn.org/api/docs/<br>
TELEGRAM_TOKEN - Токен от Telegram бота. Создать его можно через https://t.me/BotFather<br>
RESERVE_TELEGRAM_TOKEN - Токен от Telegram бота, который будет оповещать вас об ошибках. Создать его можно через https://t.me/BotFather<br>
TG_CHAT_ID - Уникальный ID чата. Узнать свой можно с помощью бота - https://t.me/userinfobot<br>

## Как запустить локально
Команда для запуска проекта локально (Linux):
```shell
python3 api.py
```

## Как запустить на сервере
Необходимо настроить демонизацию (https://dvmn.org/encyclopedia/deploy/systemd-tutorial/).
Для этого в папке `etc/systemd/system` создайте файл `notificationbot.service` с таким содержимым:

```
[Service]
ExecStart=/opt/lesson-status-notification/venv/bin/python3 /opt/lesson-status-notification/api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

ExecStart - указываем путь к python3 (который принадлежит к venv) и путь к скрипту для запуска бота (api.py)<br>
Restart - Перезапускает бота, если произошел какой-либо сбой<br>
WantedBy - Запускает бота, если сервер перезагрузился<br>

Далее запустите юнит с помощью команды:
```shell
systemctl start notificationbot
```

И добавьте юнит в автозагрузку сервера:
```shell
systemctl enable notificationbot
```

Проверить, запустился ли юнит, используйте команду:
```shell
journalctl -u notificationbot
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).