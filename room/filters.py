import django_filters
from .models import *

class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields=['name',]