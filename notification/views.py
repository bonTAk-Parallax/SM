from django.shortcuts import render
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin
from rest_framework import generics
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .tasks import send_notification_task

User = get_user_model()

# daphne -p 8000 social_media.asgi:application   
class NotificationView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_notification_task.delay(instance.id)
        # channel_layer = get_channel_layer()
        # group_name = f"user_{instance.receiver.id}"
        # print(f"Sending notification to group {group_name}")
        # async_to_sync(channel_layer.group_send)(
        #     group_name,
        #     {
        #         "type": "send_notification",
        #         "message": NotificationSerializer(instance).data
        #     }
        # ) 

    def get_queryset(self):
        read = self.request.query_params.get('read')
        if read:
            return Notification.objects.filter(receiver=self.request.user, is_read=True)
        return Notification.objects.filter(receiver=self.request.user)
    
# create notification--->take it's info send it to consumers by calling async_to_sync from views,
# which distributes it to all the consumers in the group

# List all notification, both read and unread
# filter only read/undread notifications
    

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'pk'

