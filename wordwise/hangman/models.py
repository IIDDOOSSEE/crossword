from django.db import models

# Create your models here.
from wordbank.models import wordBank
from user.models import Account

class fail_count(models.Model):
    username = models.ForeignKey(Account, on_delete=models.CASCADE)
    word = models.ForeignKey(wordBank, on_delete=models.CASCADE)
    fails = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'word'], name='unique_nw')
        ]

    def __str__(self):
        return f"{self.username.username} - {self.word.word}"