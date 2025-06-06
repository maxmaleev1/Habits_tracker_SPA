from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet
from .models import Habit
from .paginators import HabitPagination
from .serializers import HabitSerializer
from telegram_reminder.services import send_message


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if habit.user.telegram_id:
            send_message(
                habit.user.telegram_id, 'Создана новая привычка!'
            )


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.filter(is_public=True).order_by('-id')
