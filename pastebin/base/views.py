from django.shortcuts import render, redirect, get_object_or_404
from .models import Room


# Create your views here.
def create_room(request):
    room = Room.objects.create()  # Automatically create a new room
    return redirect('room_detail', room_id=room.room_id)


def room_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    return render(request, 'room_detail.html', {'room': room})