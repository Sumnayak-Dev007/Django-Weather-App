from django.urls import path
from .views import Home_view

urlpatterns = [
    path('weather/',Home_view,name='weather'),
]