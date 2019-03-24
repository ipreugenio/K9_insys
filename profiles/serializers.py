from rest_framework import serializers
from unitmanagement.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = 'id', 'k9', 'user', 'position', 'message', 'viewed', 'datetime'