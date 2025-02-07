from django.urls import path
from .views import hangman_game, guess_letter, reset_game
app_name = "hangman"
urlpatterns = [
    path('', hangman_game, name='hangman_game'),
    path('guess/', guess_letter, name='guess_letter'),
    path('reset/', reset_game, name='reset_game'),
]
