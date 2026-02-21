from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('new/', views.create_new_game, name='new_game'),
    path('game/<int:pk>/', views.load_game, name='game')
]
