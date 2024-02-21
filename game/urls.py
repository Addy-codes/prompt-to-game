from django.urls import path
from .views import *

urlpatterns = [
    path('my-games/', MyGames.as_view(), name='mygames_list'),
    path('all-games/', UGGameListView.as_view(), name='games_list'),
    path('create-direct-game/', CreateDirectGame.as_view(), name='CreateDirectGame'),
]
