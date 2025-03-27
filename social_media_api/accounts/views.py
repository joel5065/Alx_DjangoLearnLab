from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserProfileSerializer
from .models import CustomUser
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
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

class UserViewSet(viewsets.ModelViewSet):
    queryset =CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserProfileSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['follow', 'unfollow', 'following', 'followers']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        if request.user.follow(user_to_follow):
            return Response({'status': 'following'})
        return Response(
            {'error': 'Already following or cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        if request.user.unfollow(user_to_unfollow):
            return Response({'status': 'unfollowed'})
        return Response(
            {'error': 'Not following this user'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True)
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)