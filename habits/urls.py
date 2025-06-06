from django.urls import path
from rest_framework.routers import SimpleRouter

from .apps import HabitsConfig
from .views import PublicHabitListView, HabitViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register('', HabitViewSet, basename='habit')

urlpatterns = [
    path('public/', PublicHabitListView.as_view(), name='public_habit_list'),
]

urlpatterns += router.urls
