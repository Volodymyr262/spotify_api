from django.shortcuts import render, redirect
import shortuuid
from .models import Room
from django.utils import timezone


def create_room(request):
    unique_id = shortuuid.ShortUUID().random(length=8)
    return redirect(f'/{unique_id}/')


def editor(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    if room.is_expired():
        return render(request, 'expired.html')

    created_at = room.created_at.strftime('%Y-%m-%d %H:%M:%S')
    expires_at = (room.created_at + timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'editor.html', {
        'room_name': room_name,
        'created_at': created_at,
        'expires_at': expires_at,
    })
