from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.test import APITestCase
from habits.models import Habit
from habits.validators import (validate_duration, validate_periodicity,
                               validate_related_award_pleasant)


User = get_user_model()


class BaseHabitTestCase(APITestCase):
    '''
    Базовый тестовый класс с методом setUp для создания пользователя и
    приятной привычки.
    '''
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@user.com', password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='08:00:00',
            action='Test pleasant habit',
            is_pleasant=True,
            duration=60,
            periodicity=1,
        )


class ValidatorsTestCase(BaseHabitTestCase):
    '''Тесты для кастомных валидаторов привычек'''

    def test_related_award(self):
        '''
        Нельзя указывать одновременно связанную привычку и награду
        '''
        data = {
            'award': 'Coffee',
            'related': self.pleasant_habit.id,
            'is_pleasant': False,
        }
        with self.assertRaises(serializers.ValidationError) as context:
            validate_related_award_pleasant(data)
        self.assertIn(
            'Нельзя одновременно указывать связанную привычку и '
            'вознаграждение',
            str(context.exception),
        )

    def test_pleasant_award(self):
        '''У приятной привычки не может быть вознаграждения'''
        data = {'is_pleasant': True, 'award': 'Chocolate'}
        with self.assertRaises(serializers.ValidationError) as context:
            validate_related_award_pleasant(data)
        self.assertIn(
            'У приятной привычки не может быть вознаграждения',
            str(context.exception),
        )

    def test_pleasant_related(self):
        '''У приятной привычки не может быть связанной привычки.'''
        data = {'is_pleasant': True, 'related': self.pleasant_habit.id}
        with self.assertRaises(serializers.ValidationError) as context:
            validate_related_award_pleasant(data)
        self.assertIn(
            'У приятной привычки не может быть связанной привычки',
            str(context.exception),
        )

    def test_duration(self):
        '''Время выполнения не может превышать 120 секунд.'''
        with self.assertRaises(serializers.ValidationError) as context:
            validate_duration(121)
        self.assertIn(
            'Время выполнения не может превышать 120 секунд.',
            str(context.exception)
        )

    def test_periodicity_low(self):
        '''Периодичность не может быть меньше 1 дня.'''
        with self.assertRaises(serializers.ValidationError) as context:
            validate_periodicity(0)
        self.assertIn(
            'Периодичность должна быть от 1 до 7 дней.',
            str(context.exception)
        )

    def test_periodicity_high(self):
        '''Периодичность не может превышать 7 дней.'''
        with self.assertRaises(serializers.ValidationError) as context:
            validate_periodicity(8)
        self.assertIn(
            'Периодичность должна быть от 1 до 7 дней.',
            str(context.exception)
        )


class HabitModelTestCase(BaseHabitTestCase):
    '''Тесты для модели Habit и её метода clean'''

    def test_create_valid_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Office',
            time='09:00:00',
            action='Test action',
            duration=90,
            periodicity=2,
            award='Coffee',
        )
        self.assertEqual(habit.action, 'Test action')
        self.assertEqual(habit.periodicity, 2)

    def test_str_representation(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Park',
            time='15:00:00',
            action='Evening walk',
            duration=30,
            periodicity=1,
        )
        self.assertEqual(str(habit), 'Evening walk в 15:00:00 в Park')

        habit.time = '09:00:00'
        habit.place = 'Office'
        habit.save()
        self.assertEqual(str(habit), 'Evening walk в 09:00:00 в Office')
