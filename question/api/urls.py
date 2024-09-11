from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('questions',QuestionViewSet,basename='questions')
router.register('answers',AnswerViewSet,basename='answers')
router.register('votes',VotesViewSet,basename='votes')
urlpatterns = [
    path('', include(router.urls)),#post
]
