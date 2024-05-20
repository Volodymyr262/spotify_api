from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=8, unique=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name