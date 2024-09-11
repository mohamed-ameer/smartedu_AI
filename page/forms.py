from django import forms
from page.models import Page

class NewPageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    # video_url = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), initial='Your name',required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    # files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    class Meta:
        model = Page
        fields = ('title','video_url','description', 'file')

