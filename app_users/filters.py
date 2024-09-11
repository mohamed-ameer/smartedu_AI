from attr import fields
import django_filters
from .models import *

class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields=['phone', 'college_id', 'linkedin']