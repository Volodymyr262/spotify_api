from django.urls import path
from . import views

urlpatterns = [
    #path('', views.create_room, name='create_room'),
    path('<str:room_id>/', views.room_detail, name='room_detail'),
    path('', views.index)
]