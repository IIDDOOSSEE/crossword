from django.contrib import admin
from .models import Account

class UserManage(admin.ModelAdmin):
    filter_horizontal = ('flashcard',)  # Improves selection UI

# Check if the model is already registered
if not admin.site.is_registered(Account):
    admin.site.register(Account, UserManage)
