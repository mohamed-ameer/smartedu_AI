from rest_framework import viewsets
from .serializers import *
from completion.models import *

class CompletionViewSet(viewsets.ModelViewSet):
    queryset = Completion.objects.all()
    serializer_class = CompletionSerializer