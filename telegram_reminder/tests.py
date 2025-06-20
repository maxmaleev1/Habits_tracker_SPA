from datetime import datetime, timedelta
from unittest.mock import patch
import pytz
import requests
from django.conf import settings
from habits.models import Habit
from telegram_reminder.services import send_message
from telegram_reminder.tasks import send_reminders
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from telegram_reminder.models import TelegramReminder
from django.utils import timezone


User = get_user_model()


class TelegramReminderCase(APITestCase):
    '''Тесты приложения для отправки напоминаний в Telegram'''

    @patch('telegram_reminder.services.requests.get')
    def test_send_successful_message(self, mock_get):
        mock_get.return_value.status_code = 200
        result = send_message('12345', 'Test')
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('telegram_reminder.services.requests.get')
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

        now = timezone.now()
        habit_time = now.time()

        self.habit = Habit.objects.create(
            user=self.user,
            place='Большая комната',
            time=habit_time,
            action='Разминка',
            duration=60,
            periodicity=1,
        )

        self.reminder = TelegramReminder.objects.create(
            user=self.user,
            habit=self.habit,
            reminder_text='Сделай разминку!',
            award_text='Молодец, награда!'
        )

    @patch('telegram_reminder.tasks.send_message')
    def test_message_sends_and_updates_time(self, mock_send):
        old_time = self.habit.time

        send_reminders()

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
