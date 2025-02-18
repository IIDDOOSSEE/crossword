from django.urls import path
from . import views
app_name = "hangman"
urlpatterns = [
    path('', views.hangman_game, name='hangman_game'),
    path('guess/', views.guess_letter, name='guess_letter'),
    path('reset/', views.reset_game, name='reset_game'),
    path('save-fail-count/',views.save_fail_count, name='save_fail_count'),
]
