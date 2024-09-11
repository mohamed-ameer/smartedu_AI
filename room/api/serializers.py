from rest_framework import serializers
from room.models import *
# get put update delete Room data
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'
# get put update delete Message data        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields='__all__'