from rest_framework import serializers
from assignment.models import *
# get put update delete Assignment data
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Assignment
        fields='__all__'
# get put update delete Submission data        
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submission
        fields='__all__'