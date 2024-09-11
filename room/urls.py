from django.urls import path

from . import views

urlpatterns = [
    path('<course_id>/rooms', views.rooms, name='rooms'),
    path('<course_id>/addroom/', views.NewRoom, name='newroom'),
    path('<slug:slug>/', views.room, name='room'),
]