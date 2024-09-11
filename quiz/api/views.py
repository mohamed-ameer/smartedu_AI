from rest_framework import viewsets
from .serializers import *
from quiz.models import *

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuizzesViewSet(viewsets.ModelViewSet):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer

class AttempterViewSet(viewsets.ModelViewSet):
    queryset = Attempter.objects.all()
    serializer_class = AttempterSerializer

class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
