from rest_framework import  serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
    
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user
        def get_token(self, obj):
            token = Token.objects.get(user=obj)
            return token.key