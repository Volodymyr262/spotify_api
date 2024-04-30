from django.shortcuts import render, redirect, get_object_or_404
from .models import Room


# create room obj and redirect to the room page
def create_room(request):
    room = Room.objects.create()  # Automatically create a new room
    return redirect('room_detail', room_id=room.room_id)


# room page
def room_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    return render(request, 'room_detail.html', {'room': room})


def index(request):
    return render(request, 'index.html', context={'text': 'Hello World'})