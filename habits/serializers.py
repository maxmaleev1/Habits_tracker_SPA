from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    validate_duration, validate_periodicity, validate_related_award_pleasant
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']

    def validate_related_award_pleasant(self, data):
        return validate_related_award_pleasant(data)

    def validate_duration(self, value):
        return validate_duration(value)

    def validate_periodicity(self, value):
        return validate_periodicity(value)
