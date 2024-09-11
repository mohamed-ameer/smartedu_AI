from posixpath import basename
from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('post_files',PostFileContentViewSet,basename='post_files')
router.register('page',PageViewSet,basename='page')
router.register('comments',CommentViewSet,basename='comments')
router.register('replies',ReplyViewSet,basename='replies')
urlpatterns = [
    path('', include(router.urls)),#post
]
