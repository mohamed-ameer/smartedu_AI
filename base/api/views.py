from rest_framework import viewsets
from .serializers import *
from base.models import *

class RoomMemberViewSet(viewsets.ModelViewSet):
    queryset = RoomMember.objects.all()
    serializer_class = RoomMemberSerializer
