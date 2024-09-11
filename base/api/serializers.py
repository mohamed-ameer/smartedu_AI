from rest_framework import serializers
from base.models import *
# get put update delete RoomMember data
class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoomMember
        fields=['room_name','name']
