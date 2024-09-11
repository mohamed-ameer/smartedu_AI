from rest_framework import serializers
from completion.models import *
# get put update delete Completion data
class CompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Completion
        fields='__all__'
