from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('profiles',ProfileViewSet,basename='profiles')
urlpatterns = [
    path('signup/',SignupView.as_view()),#post 
    path('login/',CustomAuthToken.as_view(), name='auth-token'),#post
    path('logout/', LogoutView.as_view(), name='logout-view'),#post
    path('', include(router.urls)),#post

]
