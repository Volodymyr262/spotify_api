from django.shortcuts import render, redirect
import shortuuid


def create_room(request):
    unique_id = shortuuid.ShortUUID().random(length=8)
    return redirect(f'/{unique_id}/')


def editor(request, room_name):
    return render(request, 'editor.html', {'room_name': room_name})