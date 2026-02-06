from .models import *
from app_users.models import *
from post.models import *
from post.serializers import *
from rest_framework import serializers


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    receiver = UserOfPost(fields=['username', 'profile_pic'], read_only=True)
    triggerer = UserOfPost(fields=['username', 'profile_pic'], read_only=True)
    
    class Meta:
        model = Notification
        fields = ['url','receiver', 'notif_type', 'created_at', 'is_read', 'triggerer']
        read_only_fields = ['receiver', 'notif_type', 'created_at', 'triggerer']