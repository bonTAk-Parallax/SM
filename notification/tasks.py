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
def process_mentions(usernames, triggerer_id):
    print("TASKS.PY FOR MENTION PROCESS ACTIVATED!!!")
    users = User.objects.filter(username__in = usernames)
    print(users)
    triggerer = User.objects.get(id=triggerer_id)
    print(f"the triggerer here is {triggerer}")
    # .exclude(id= triggerer.id)
    for user in users:
        notification=Notification.objects.create(
            receiver = user,
            triggerer = triggerer,
            notif_type = f"{user.username} mentioned you.",
        )
        # send_notification_task.delay(notification.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{notification.receiver.id}",
            {
                "type": "send_notification",
                "message": NotificationSerializer(
                    notification, context={"request": None}
                ).data
            }
        )

# mention worked but need to pass the link to the post/comment/reply in it's url 
# disable being able to mention oneself and also the hardcoded user for testing in consumer
# delete notification if that post/comment/reply is deleted