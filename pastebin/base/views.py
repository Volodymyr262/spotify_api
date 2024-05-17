from django.shortcuts import render, redirect

def home(request):
    return redirect('editor', room_name='default')

def editor(request, room_name):
    return render(request, 'editor.html', {'room_name': room_name})
