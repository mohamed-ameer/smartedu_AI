from django import forms
from classroom.models import Course, Category


class NewCourseForm(forms.ModelForm):
	picture = forms.ImageField(required=True)
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	secret_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
	category = forms.ModelChoiceField(queryset=Category.objects.all())

	class Meta:
		model = Course
		fields = ('picture', 'title','secret_code','description','university','major_types','category')

