from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('home/', views.home, name='home'),
    path('<str:room_name>/', views.editor, name='editor'),
]
