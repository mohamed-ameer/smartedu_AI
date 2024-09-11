from rest_framework import serializers
from quiz.models import *
# get put update delete Answer data
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields='__all__'
# get put update delete Question data        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'
# get put update delete Quizzes data        
class QuizzesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quizzes
        fields='__all__'
# get put update delete Attempter data        
class AttempterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attempter
        fields='__all__'
# get put update delete Attempter data        
class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attempt
        fields='__all__'