# Определяет схемы urls для пользователей

from django.urls import path, include

app_name = 'accounts'
urlpatterns = [
    # Включить urls авторизации автоматически
    path('', include('django.contrib.auth.urls')),
]
