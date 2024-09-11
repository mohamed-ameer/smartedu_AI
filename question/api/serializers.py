from rest_framework import serializers
from question.models import *
# get put update delete Question data
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'
# get put update delete Answer data        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields='__all__'
# get put update delete Votes data        
class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Votes
        fields='__all__'