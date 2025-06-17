from django.urls import path
from .apps import TelegramReminderConfig
from .services import send_message


app_name = TelegramReminderConfig.name

urlpatterns = [
    path('send_message/', send_message, name='send_message'),
]
