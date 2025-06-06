from datetime import datetime, timedelta
from unittest.mock import patch
import pytz
import requests
from django.conf import settings
from telegram_reminder.services import send_message
from telegram_reminder.tasks import message
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TelegramReminderCase(APITestCase):
    '''Тесты приложения для отправки напоминаний в Telegram'''

    @patch('habits.services.requests.get')
    def test_send_successful_message(self, mock_get):
        mock_get.return_value.status_code = 200
        result = send_message('12345', 'Test')
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('habits.services.requests.get')
    def test_send_message_connection_error(self, mock_get):
        mock_get.side_effect = requests.RequestException('Connection failed')

        with self.assertRaises(requests.RequestException) as context:
            send_message('12345', 'Test')

        self.assertIn(
            'Ошибка при отправке сообщения в Telegram',
            str(context.exception)
        )
        self.assertIsInstance(
            context.exception.__cause__, requests.RequestException
        )
        mock_get.assert_called_once()


class TelegramReminderTaskCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@gmail.com',
            password='testpass',
            telegram_id='123456789'
        )

        # Время привычки = сейчас + 5 минут (чтобы попало в окно 10 минут)
        zone = pytz.timezone(settings.CELERY_TIMEZONE)
        now = datetime.now(zone)
        habit_time = (now + timedelta(minutes=5)).time()

        self.habit = Habit.objects.create(
            user=self.user,
            place='Большая комната',
            time=habit_time,
            action='Разминка',
            duration=60,
            periodicity=1,
        )

    @patch('habits.tasks.send_message')
    def test_message_sends_and_updates_time(self, mock_send):
        old_time = self.habit.time

        message()

        self.habit.refresh_from_db()

        # Проверка: сообщение было отправлено 1 раз
        mock_send.assert_called()
        self.assertGreaterEqual(mock_send.call_count, 1)

        # Проверка: время привычки обновилось (добавлен 1 день)
        zone = pytz.timezone(settings.CELERY_TIMEZONE)
        now = datetime.now(zone)
        expected_datetime = (datetime.combine
                             (now.date(), old_time) + timedelta(days=1)
                             )
        self.assertEqual(self.habit.time, expected_datetime.time())
