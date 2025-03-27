from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        })
    return Response("errors during user creation")
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get(['username'])
    password = request.data.get(['password'])
    user = authenticate(username=username, password=password)

    if user:
        token, _=Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response("Error: Invalid credentials!")