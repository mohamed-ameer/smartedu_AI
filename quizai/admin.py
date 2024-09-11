from django.contrib import admin
from quiz.models import *
from quizai.models import AnswerAI, AttemptAI, AttempterAI, QuestionAI, QuizzesAI

# Register your models here.
admin.site.register(AnswerAI)
admin.site.register(QuestionAI)
admin.site.register(QuizzesAI)
admin.site.register(AttemptAI)
admin.site.register(AttempterAI)