from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from post.models import Comment
from .serializers import NotificationSerializer
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_notification_task(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        channel_layer = get_channel_layer()
        group_name = f"user_{notification.receiver.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": NotificationSerializer(
                    notification, context={'request': None}).data
            }
        )
    except Notification.DoesNotExist:
        pass

@shared_task
def process_mentions(usernames, triggerer):
    users = User.objects.filter(username__in = usernames)
    # .exclude(id= triggerer.id)
    for user in users:
        notification=Notification.objects.create(
            receiver = user,
            triggerer = triggerer,
            notif_type = f"{user} mentioned you.",
        )
        send_notification_task(notification_id=notification.id)