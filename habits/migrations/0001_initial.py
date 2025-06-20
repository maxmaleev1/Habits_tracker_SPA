# Generated by Django 5.2.2 on 2025-06-17 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=255, verbose_name='Место')),
                ('time', models.TimeField(verbose_name='Время')),
                ('action', models.CharField(max_length=255, verbose_name='Действие')),
                ('is_pleasant', models.BooleanField(default=False, verbose_name='Приятная привычка')),
                ('periodicity', models.PositiveIntegerField(default=1, verbose_name='Периодичность в днях')),
                ('award', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вознаграждение')),
                ('duration', models.PositiveIntegerField(verbose_name='Время на выполнение в секундах')),
                ('is_public', models.BooleanField(default=False, verbose_name='Публичность привычки')),
                ('related', models.ForeignKey(blank=True, limit_choices_to={'is_pleasant': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_to', to='habits.habit')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
            },
        ),
    ]
