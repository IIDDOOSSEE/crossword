from django.urls import path
from . import views

app_name = "user"  # This is required for namespacing

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("info/", views.get_user_info, name="user-info")
]
