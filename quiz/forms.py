from django import forms
from quiz.models import Quizzes, Question, Answer
from django.forms.widgets import NumberInput
class NewQuizForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	start_time=forms.DateTimeField(widget=NumberInput(attrs={'type': 'datetime-local'}), required=True)
	end_time=forms.DateTimeField(widget=NumberInput(attrs={'type': 'datetime-local'}), required=True)
	class Meta:
		model = Quizzes
		fields = ('title','start_time','end_time')


class NewQuestionForm(forms.ModelForm):
	question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	points = forms.IntegerField(max_value=100, min_value=1)

	class Meta:
		model = Question
		fields = ('question_text', 'points')