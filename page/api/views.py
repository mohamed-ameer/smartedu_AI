from rest_framework import viewsets
from .serializers import *
from page.models import *

class PostFileContentViewSet(viewsets.ModelViewSet):
    queryset = PostFileContent.objects.all()
    serializer_class = PostFileContentSerializer

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
