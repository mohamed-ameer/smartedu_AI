from rest_framework import serializers
from app_users.models import *
# get put update delete profile data
class GetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

# authentication
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['user_type',]
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username', 'email', 'password', 'password2','profile']
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.save()
        return user

