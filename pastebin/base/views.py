# views.py
from django.shortcuts import render, redirect
from .models import Room, TextSnippet

def home(request):
    # Generate a new room with a unique 6-character ID
    new_room = Room()
    new_room.save()
    return redirect('editor', room_name=new_room.room_id)

def editor(request, room_name):
    room, created = Room.objects.get_or_create(room_id=room_name)
    snippet, created = TextSnippet.objects.get_or_create(room=room)
    return render(request, 'editor.html', {'room_name': room_name})
