from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("hangman/",include("hangman.urls")),
    path("",include("menu.urls")),
    path("admin/", admin.site.urls)
]
