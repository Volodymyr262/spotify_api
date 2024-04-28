from django.db import models
import random
import string


class Room(models.Model):
    room_id = models.CharField(max_length=8, primary_key=True, unique=True)

    def generate_unique_id(self):
        characters = string.ascii_letters + string.digits
        while True:
            room_id = ''.join(random.choice(characters) for _ in range(8))
            if not Room.objects.filter(room_id=room_id).exists():
                return room_id

    def save(self, *args, **kwargs):
        if not self.room_id:
            self.room_id = self.generate_unique_id()
        super().save(*args, **kwargs)