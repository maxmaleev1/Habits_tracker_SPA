from django.db import models
from config import settings
from habits.models import Habit


class TelegramReminder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits_reminder',
    )
    habit = models.ForeignKey(
        'habits.Habit',
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    reminder_text = models.TextField(
        f'Напоминание: Необходимо выполнить {Habit.action} в'
        f' {Habit.time} в {Habit.place}'
    )
    award_text = models.TextField(
        f'После выполнения получите награду: {Habit.award}'
    )

    def __str__(self):
        return f'Напоминание в Телеграм {self.user} о {self.habit}'

    class Meta:
        verbose_name = 'Телеграм напоминание'
