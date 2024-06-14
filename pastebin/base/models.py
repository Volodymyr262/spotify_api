from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.

    def __str__(self):
        return self.name

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(days=1)