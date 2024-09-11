from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('category',CategoryViewSet,basename='category')
router.register('course',CourseViewSet,basename='submissions')
router.register('grade',GradeViewSet,basename='grade')
urlpatterns = [
    path('', include(router.urls)),#post
]
