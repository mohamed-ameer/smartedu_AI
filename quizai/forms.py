from django import forms
from quizai.models import *
class NewQuizForm(forms.ModelForm):
    context = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    points = forms.IntegerField(max_value=100, min_value=1)
    class Meta:
        model = QuizzesAI
        fields = ('context', 'file', 'points')

class NewQuestionForm(forms.ModelForm):
	question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	points = forms.IntegerField(max_value=100, min_value=1)

	class Meta:
		model = QuestionAI
		fields = ('question_text',)
