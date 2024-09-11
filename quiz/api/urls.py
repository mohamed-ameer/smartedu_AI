from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('answers',AnswerViewSet,basename='answers')
router.register('questions',QuestionViewSet,basename='questions')
router.register('quizzes',QuizzesViewSet,basename='quizzes')
router.register('attempter',AttempterViewSet,basename='attempter')
router.register('attempts',AttemptViewSet,basename='attempts')
urlpatterns = [
    path('', include(router.urls)),#post
]
