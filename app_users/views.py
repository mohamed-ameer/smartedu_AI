from cgitb import html
from email import message
from django.shortcuts import render, redirect, get_object_or_404
from app_users.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from .models import *
from .filters import ProfileFilter
from django.views.generic import CreateView
from .forms import *
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def NavInfo(request):
	user = request.user
	nav_profile = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=request.user)
	
	return {'nav_profile': nav_profile}

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")
            # return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'app_users/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Create your views here.
# def index(request):
#     return render(request,'app_users/index.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileInfoForm(data=request.POST)

        # if user_form.is_valid() and profile_form.is_valid():
        if user_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            user.save()

            # profile = profile_form.save(commit=False)
            # profile.user = user
            # profile.save()

            registered = True
            return render(request, 'app_users/login.html')
        else:
            # print(user_form.errors, profile_form.errors)
            print(user_form.errors)
    else:
        user_form = UserForm()
        # profile_form = UserProfileInfoForm()

    # return render(request, 'app_users/registration.html',
    #                         {'registered':registered,
    #                          'user_form':user_form,
    #                          'profile_form':profile_form})
    return render(request, 'app_users/registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'captcha':FormWithCaptcha
                            })

class HomeView(TemplateView):
    template_name = 'app_users/index.html'

# class ContactView(CreateView):
#     model = Contact
#     fields = '__all__'  
#     template_name = 'app_users/contact.html'


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            Contact.objects.create(name=name, email=email, message=message)
            html = render_to_string('app_users/contactsent.html',{'name':name,'email':email,'message':message})
            # send_mail(
            #     name,
            #     message,
            #     email,
            #     [settings.EMAIL_HOST_USER],
            # )
            send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            [settings.EMAIL_HOST_USER],
            html_message=html,
            )
            return redirect('index')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request,'app_users/contact.html',context)

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'app_users/profile.html',{'profile': profile})



def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method=='POST':
        userform = UserEditForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect(reverse('profile'))

    else :
        userform = UserEditForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request,'app_users/profile_edit.html',{'userform':userform , 'profileform':profileform})

@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'registration/change_password_done.html')


# @login_required
# def EditProfile(request):
# 	user = request.user.id
# 	profile = Profile.objects.get(user__id=user)
# 	user_basic_info = User.objects.get(id=user)

# 	if request.method == 'POST':
# 		form = EditProfileForm(request.POST, request.FILES, instance=profile)
# 		if form.is_valid():
# 			profile.picture = form.cleaned_data.get('picture')
# 			profile.banner = form.cleaned_data.get('banner')
# 			user_basic_info.first_name = form.cleaned_data.get('first_name')
# 			user_basic_info.last_name = form.cleaned_data.get('last_name')
# 			profile.location = form.cleaned_data.get('location')
# 			profile.url = form.cleaned_data.get('url')
# 			profile.profile_info = form.cleaned_data.get('profile_info')
# 			profile.save()
# 			user_basic_info.save()
# 			return redirect('index')
# 	else:
# 		form = EditProfileForm(instance=profile)

# 	context = {
# 		'form':form,
# 	}

# 	return render(request, 'registration/edit_profile.html', context)