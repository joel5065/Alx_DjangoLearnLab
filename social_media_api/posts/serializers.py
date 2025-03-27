from .models import Comment, Post
from accounts.serializers import UserSerializer
from rest_framework import serializers

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