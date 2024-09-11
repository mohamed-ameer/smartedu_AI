from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('rooms',RoomViewSet,basename='rooms')
router.register('messages',MessageViewSet,basename='messages')
urlpatterns = [
    path('', include(router.urls)),#post
]
