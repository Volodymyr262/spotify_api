from django.db import models
import shortuuid

class Room(models.Model):
    room_id = models.CharField(max_length=22, primary_key=True, unique=True, editable=False)  # shortuuid length is 22

    def save(self, *args, **kwargs):
        if not self.room_id:
            self.room_id = shortuuid.ShortUUID().random(length=6)
        super().save(*args, **kwargs)

class TextSnippet(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    text = models.TextField(default="")
