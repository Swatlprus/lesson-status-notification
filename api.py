import requests
import time
from environs import Env
import logging

import telegram

logger = logging.getLogger('Logger')

class TelegramLogsHandler(logging.Handler):

    def __init__(self, telegram_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=telegram_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(lessons, telegram_token, tg_chat_id):
    for lesson in lessons:
        lesson_title = lesson['lesson_title']
        error = lesson['is_negative']
        url = lesson['lesson_url']
        if error:
            description = 'К сожалению в работе нашлись ошибки.'
        else:
            description = 'Преподавателю все понравилось,\
                можно приступать к следующему уроку!'
        bot = telegram.Bot(token=telegram_token)
        bot.send_message(
            chat_id=tg_chat_id,
            text=f'У вас проверили работу «{lesson_title}» \n\n{description}\
                \n\nСсылка на урок: {url}'
        )


def get_notification(dvmn_token, payload={}):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': dvmn_token}
    response = requests.get(
        url,
        headers=headers,
        timeout=90,
        params=payload,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    dvmn_token = env('DVMN_TOKEN')
    telegram_token = env('TELEGRAM_TOKEN')
    reserve_telegram_token = env('RESERVE_TELEGRAM_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(reserve_telegram_token, tg_chat_id))
    logger.info('Бот начал работу')
    payload = {}
    while True:
        try:
            review_lessons = get_notification(dvmn_token, payload)
            if review_lessons['status'] == 'timeout':
                payload = {'timestamp': review_lessons['timestamp_to_request']}
            elif review_lessons['status'] == 'found':
                lessons = review_lessons['new_attempts']
                send_message(lessons, telegram_token, tg_chat_id)
        except requests.exceptions.HTTPError:
            logger.error('Бот упал с ошибкой HTTPError')
        except requests.exceptions.ReadTimeout:
            logger.info('Wait... I will try to send the request again')
        except requests.exceptions.ConnectionError:
            logger.error('Бот упал с ошибкой ConnectionError')
            time.sleep(10)

