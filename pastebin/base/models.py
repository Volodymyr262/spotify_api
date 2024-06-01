from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    text = models.TextField(default='')

    def __str__(self):
        return self.name
