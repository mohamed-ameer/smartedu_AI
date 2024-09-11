from typing_extensions import Required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile,Contact
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),required=True)

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')

        # widgets = {
        # "password":"forms.PasswordInput()",
        # }

        labels = {
        'password1':'Password',
        'password2':'Confirm Password'
        }

class UserProfileInfoForm(forms.ModelForm):
    teacher = 'teacher'
    student = 'student'
    user_types = [
        (student, 'student'),
        (teacher, 'teacher'),
    ]
    user_type = forms.ChoiceField(required=True, choices=user_types)
    # user_type = forms.CheckboxInput(required=True, choices=user_types)

    class Meta():
        model = Profile
        fields = ('user_type',)

##############################

class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['Passwords do not match.'])
        return self.cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['username','first_name','last_name','email'] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['picture','phone','college_id','univeristy_name','major_types','facebook','github','linkedin']
class ContactForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    email=forms.EmailField()
    message=forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = Contact
        fields =['name','email','message']


# class EditProfileForm(forms.ModelForm):
# 	first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
# 	last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
# 	picture = forms.ImageField(required=False)
# 	banner = forms.ImageField(required=False)
# 	phone = forms.IntegerField(widget=forms.TextInput(), required=False)
# 	college_id = forms.IntegerField(widget=forms.TextInput(), required=False)
# 	class Meta:
# 		model = Profile
# 		fields = ('picture', 'banner', 'first_name', 'last_name','phone','college_id')
# 		# fields = ('picture', 'banner', 'first_name', 'last_name', 'location', 'url', 'profile_info')