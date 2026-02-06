from django.db import models
from django.contrib.auth import get_user_model
from post.models import *
from app_users.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

User = get_user_model()


# notification-system-42053
# https://console.firebase.google.com/u/0/project/notification-system-42053/overview
class Notification(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='content_type_notification', on_delete = models.CASCADE, null=True, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    triggerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    notif_type = models.CharField(max_length=30, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# url, generic foreign key

class WebPushToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="webpush_tokens")
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


