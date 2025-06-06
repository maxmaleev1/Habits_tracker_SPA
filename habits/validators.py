from rest_framework import serializers


def validate_related_award_pleasant(data):
    if data.get('award') and data.get('related'):
        raise serializers.ValidationError(
            'Нельзя одновременно указывать связанную привычку и вознаграждение'
        )
    if data.get('award') and data.get('is_pleasant'):
        raise serializers.ValidationError(
            'У приятной привычки не может быть вознаграждения'
        )
    if data.get('related') and data.get('is_pleasant'):
        raise serializers.ValidationError(
            'У приятной привычки не может быть связанной привычки'
        )
    return data


def validate_duration(value):
    if value > 120:
        raise serializers.ValidationError(
            'Время выполнения не может превышать 120 секунд.'
        )
    return value


def validate_periodicity(value):
    if value < 1 or value > 7:
        raise serializers.ValidationError(
            'Периодичность должна быть от 1 до 7 дней.'
        )
    return value
