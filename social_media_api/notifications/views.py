from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    target_content = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 'target_type', 'target_id', 'target', 'target_content', 'timestamp', 'unread']
        read_only_fields = ['id', 'recipient', 'actor', 'actor_username', 'verb', 'target_type', 'target_id', 'target', 'target_content', 'timestamp']

    def get_target_content(self, obj):
        if obj.target:
            return str(obj.target)
        return None

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user).order_by('-timestamp')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_as_read(request):
    user = request.user
    Notification.objects.filter(recipient=user, unread=True).update(unread=False)
    return Response({"message": "Notifications marked as read."}, status=status.HTTP_200_OK)
