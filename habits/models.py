from django.db import models
from config import settings


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка'
    )
    related = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_pleasant': True},
        related_name='related_to',
    )
    periodicity = models.PositiveIntegerField(
        default=1, verbose_name='Периодичность в днях'
    )
    award = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Вознаграждение'
    )
    duration = models.PositiveIntegerField(
        verbose_name='Время на выполнение в секундах'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичность привычки'
    )
    tg

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
