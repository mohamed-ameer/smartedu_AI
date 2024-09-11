from rest_framework import viewsets
from .serializers import *
from scheduale.models import *

class AssignmentSchedualeViewSet(viewsets.ModelViewSet):
    queryset = AssignmentScheduale.objects.all()
    serializer_class = AssignmentSchedualeSerializer

class QuizSchedualeViewSet(viewsets.ModelViewSet):
    queryset = QuizScheduale.objects.all()
    serializer_class = QuizSchedualeSerializer
