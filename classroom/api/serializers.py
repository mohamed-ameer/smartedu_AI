from rest_framework import serializers
from classroom.models import *
# get put update delete Category data
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
# get put update delete Course data        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'
# get put update delete Grade data        
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grade
        fields='__all__'