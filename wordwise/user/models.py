from django.db import models
from flashcard.models import flashCardDeck
class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    flashcard = models.ManyToManyField(flashCardDeck)  # Adjust based on needs

    def __str__(self):
        return self.username
