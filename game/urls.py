from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:id>/', views.get_player, name='player'),
    path('player/create/', views.PlayerCreate.as_view(), name='player_create'),
    path('player/<int:pk>/update/', views.PlayerUpdate.as_view(), name='player_update'),
]
