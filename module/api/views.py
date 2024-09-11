from rest_framework import viewsets
from .serializers import *
from module.models import *

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
