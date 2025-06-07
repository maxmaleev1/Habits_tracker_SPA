from celery import shared_task
from datetime import datetime, timedelta
from pytz import timezone
from django.utils import timezone as dj_timezone
from django.conf import settings
from habits.models import Habit
from telegram_reminder.models import TelegramReminder
from telegram_reminder.services import send_message
import time


@shared_task
def send_reminders():
    """
    Отправляет напоминания пользователям по привычкам, если текущее время
    попадает в заданный интервал. Также отправляет сообщение с наградой,
    если оно предусмотрено, и сдвигает время привычки вперёд по periodicity.
    """
    dj_timezone.activate(timezone(settings.CELERY_TIMEZONE))  # активация
    # таймзоны

    now = dj_timezone.localtime()  # получение текущего локального времени

    lower_bound = now - timedelta(minutes=10)  # нижняя граница по времени
    upper_bound = now + timedelta(minutes=10)  # верхняя граница по времени

    habits = Habit.objects.filter(  # выборка привычек в интервале времени
        time__gte=lower_bound.time(),
        time__lte=upper_bound.time()
    )

    for habit in habits:  # перебор всех подходящих привычек
        user = habit.user  # получение пользователя

        if not hasattr(user, 'telegram_id') or not user.telegram_id:
            continue  # пропустить, если нет telegram_id

        reminder = TelegramReminder.objects.get(  # получить объект напоминания
            user=user,
            habit=habit
        )

        reminder_text = reminder.reminder_text  # текст напоминания

        try:
            send_message(user.telegram_id, reminder_text)
            print(f"[OK] Напоминание отправлено пользователю {user.email}")

            if habit.award:  # если указана награда
                time.sleep(120)  # пауза 2 минуты
                award_text = reminder.award_text  # текст награды
                send_message(user.telegram_id, award_text)  # отправка награды
                print(
                    f"[OK] Сообщение с наградой отправлено пользователю "
                    f"{user.email}"
                )

            habit_datetime = datetime.combine(now.date(), habit.time)
            # объединение даты и времени привычки
            next_datetime = habit_datetime + timedelta(days=habit.periodicity)
            # расчёт следующего напоминания
            habit.time = next_datetime.time()  # установка нового времени
            habit.save()  # сохранение изменений

        except Exception as e:
            print(f"[ERROR] Не удалось отправить сообщение: {e}")
