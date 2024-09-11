"""smartedu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('app_users.urls')),
    path('course/', include('classroom.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),    
    path('videochat/', include('videochat.urls')),
    path('', include('base.urls')),
    path('rooms/', include('room.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/app_users/', include('app_users.api.urls')),    
    path('api/assignment/', include('assignment.api.urls')),    
    path('api/base/', include('base.api.urls')),    
    path('api/classroom/', include('classroom.api.urls')),    
    path('api/completion/', include('completion.api.urls')),    
    path('api/module/', include('module.api.urls')),    
    path('api/page/', include('page.api.urls')),    
    path('api/question/', include('question.api.urls')),    
    path('api/quiz/', include('quiz.api.urls')),    
    path('api/room/', include('room.api.urls')),    
    path('api/scheduale/', include('scheduale.api.urls')),    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
