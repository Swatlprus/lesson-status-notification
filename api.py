import requests
import time
import json
from environs import Env

import telegram


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


def get_notification(dvmn_token, telegram_token, chat_id, payload={}):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': dvmn_token}
    response = requests.get(
        url,
        headers=headers,
        timeout=95,
        params=payload,
    )
    response.raise_for_status()
    dvmn_response = json.loads(response.text)
    if dvmn_response['status'] == 'timeout':
        payload = {'timestamp': dvmn_response['timestamp_to_request']}
        get_notification(dvmn_token, payload)
    elif dvmn_response['status'] == 'found':
        lessons = dvmn_response['new_attempts']
        send_message(lessons, telegram_token, chat_id)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    dvmn_token = env('DVMN_TOKEN')
    telegram_token = env('TELEGRAM_TOKEN')
    tg_chat_id = env('CHAT_ID')
    while True:
        try:
            get_notification(dvmn_token, telegram_token, tg_chat_id)
        except requests.exceptions.HTTPError as err:
            print('Ooops. HTTP Error occurred')
            print('Response is: {content}'.format(content=err.response.content))
        except requests.exceptions.ReadTimeout as err:
            print('Ooops. ReadTimeout Error occurred')
            print('Response is: {content}'.format(content=err))
            print('Wait... I will try to send the request again')
            time.sleep(10)
        except requests.exceptions.ConnectionError as err:
            print('Ooops. ConnectionError occurred')
            print('Response is: {content}'.format(content=err))
            print('Wait... I will try to send the request again')
            time.sleep(10)