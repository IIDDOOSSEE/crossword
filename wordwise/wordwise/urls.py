from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("crossword/",include("crossword.urls")),
    path("admin/", admin.site.urls)
]
