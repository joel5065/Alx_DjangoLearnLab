from rest_framework import  serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 
                 'following_count', 'followers_count', 'is_following']
        read_only_fields = ['id', 'following_count', 'followers_count', 'is_following']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = get_user_model().objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user
        def get_token(self, obj):
            token = Token.objects.get(user=obj)
            return token.key
        def get_following_count(self, obj):
            return obj.get_following_count()

    def get_followers_count(self, obj):
        return obj.get_followers_count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False

class UserProfileSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['date_joined', 'last_login']
