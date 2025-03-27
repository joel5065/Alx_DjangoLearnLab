from rest_framework import  serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Comment, Post
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = get_user_model().objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user
        def get_token(self, obj):
            token = Token.objects.get(user=obj)
            return token.key
        

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'author']
        read_only_fields = ['create_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at','author', 'comments', 'comment_counts']
        read_only_fields = ['created_at', 'updated_at']

    def get_comment_count(self, obj):
        return obj.comments.count()