from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status,viewsets
from rest_framework.permissions import BasePermission,AllowAny, SAFE_METHODS
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import *
from app_users.models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

class SignupView(generics.GenericAPIView):
    serializer_class=UserSerializer 
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "profile":Profile.objects.get(user=user).user_type,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        profile, created=Profile.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'profile':profile.user_type
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

# ##################################################################
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = GetProfileSerializer
