from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('assignments',AssignmentViewSet,basename='assignments')
router.register('submissions',SubmissionViewSet,basename='submissions')
urlpatterns = [
    path('', include(router.urls)),#post
]
