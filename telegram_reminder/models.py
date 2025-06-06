from django.db import models
from config import settings
from habits.models import Habit


class TelegramReminder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
    )
    habit = models.ForeignKey(
        'habits.Habit',
        on_delete=models.CASCADE,
        related_name='reminders'
    ),
    reminder_message=models.TextField(
        f'Напоминание: Необходимо выполнить'
                             f' {habit.action} в '
                 f'{habit.time.strftime('%H:%M')} в {habit.place}'
    ),
    award_message=models.TextField(
        f'После выполнения получите награду:'f' {habit.award}'
    )

    def __str__(self):
        return f'Напоминание в Телеграм {self.user} о {self.habit}'

    class Meta:
        verbose_name = 'Телеграм напоминание'
