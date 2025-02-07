from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("", views.index, name="index"),  # Menu page
    # path("info/", views.get_user_info, name="user_info"),  # Fetch user info API/
]