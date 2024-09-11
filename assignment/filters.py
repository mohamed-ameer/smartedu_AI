import django_filters
from classroom.models import *

class GradeFilter(django_filters.FilterSet):
    class Meta:
        model = Grade
        fields=['status',]