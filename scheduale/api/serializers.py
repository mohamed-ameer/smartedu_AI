from rest_framework import serializers
from scheduale.models import *
# get put update delete AssignmentScheduale data
class AssignmentSchedualeSerializer(serializers.ModelSerializer):
    class Meta:
        model=AssignmentScheduale
        fields='__all__'
# get put update delete QuizScheduale data        
class QuizSchedualeSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizScheduale
        fields='__all__'