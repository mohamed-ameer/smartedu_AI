import django_filters
from .models import *
from app_users.models import Profile
class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields=['title','university','major_types','category']
class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields=['college_id',]

