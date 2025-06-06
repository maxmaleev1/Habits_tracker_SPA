from django.db import models


class TelegramReminder(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='telegram_reminders'
    )
    chat_id = models.CharField(max_length=255, verbose_name='Chat ID')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
