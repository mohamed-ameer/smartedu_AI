from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('assignments_scheduale',AssignmentSchedualeViewSet,basename='assignments_scheduale')
router.register('quizes_scheduale',QuizSchedualeViewSet,basename='quizes_scheduale')
urlpatterns = [
    path('', include(router.urls)),#post
]
