import requests
from config import settings


def send_message(chat_id, message):
    '''Отправка сообщений в Telegram'''
    url = f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        error_msg = f'Ошибка при отправке сообщения в Telegram: {e}'
        raise requests.RequestException(error_msg) from e
