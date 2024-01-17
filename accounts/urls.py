from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # Включить urls авторизации автоматически
    path('', include('django.contrib.auth.urls')),
    # Страница регистрации
    path('register/', views.register, name='register'),
]
