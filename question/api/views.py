from rest_framework import viewsets
from .serializers import *
from question.models import *

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class VotesViewSet(viewsets.ModelViewSet):
    queryset = Votes.objects.all()
    serializer_class = VotesSerializer
