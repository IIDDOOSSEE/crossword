from django.urls import path

from . import views

app_name = "crossword"

urlpatterns = [
    #path("", views.index, name="index"),
    path("puzzle", views.puzzle,name="puzzle")
    
]