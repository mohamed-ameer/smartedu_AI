from rest_framework import serializers
from page.models import *
# get put update delete PostFileContent data
class PostFileContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostFileContent
        fields='__all__'
# get put update delete Page data        
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields='__all__'
# get put update delete Comment data        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'
# get put update delete Reply data        
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=Reply
        fields='__all__'