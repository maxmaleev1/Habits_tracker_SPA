from datetime import datetime, timedelta
import pytz
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits.models import Habit
from telegram_reminder.models import TelegramReminder
from telegram_reminder.services import send_message


@shared_task()
def message():
    timezone.activate(pytz.timezone(settings.CELERY_TIMEZONE))
    zone = pytz.timezone(settings.CELERY_TIMEZONE)
    now_time = datetime.now(zone)

    habits = Habit.objects.all()

    for habit in habits:
        user_tg = habit.user.telegram_id

        # Собираем datetime из даты сегодня и времени из habit.time
        habit_datetime = datetime.combine(now_time.date(), habit.time)
        habit_datetime = zone.localize(habit_datetime)

        if (
            user_tg
            and now_time >= habit_datetime - timedelta(minutes=10)
            and now_time <= habit_datetime + timedelta(minutes=10)
        ):
            message = TelegramReminder.objects.get(reminder_message)
            send_message(user_tg, message)

            if habit.award:
                message = TelegramReminder.objects.get(award_message)
                send_message(user_tg, message)

            # Следующий день сдвигается по periodicity
            next_datetime = habit_datetime + timedelta(days=habit.periodicity)
            habit.time = next_datetime.time()
            habit.save()
