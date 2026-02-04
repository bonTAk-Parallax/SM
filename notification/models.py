from django.db import models
from django.contrib.auth import get_user_model
from post.models import *
from app_users.models import *

# Create your models here.

User = get_user_model()


# notification-system-42053
# https://console.firebase.google.com/u/0/project/notification-system-42053/overview
class Notification(models.Model):
    NOTIF_TYPES = [
        ("follow", "Follow"),
        ("post_comment", "Post Comment"),
        ("post_like", "Post Like"),
        ("comment_reply", "Comment Reply"),
        ("comment_like", "Comment Like"),
        ("reply_reply", "Reply Reply"),
        ("reply_like", "Reply Like"),
        ("mention", "Mention")
    ]

    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    triggerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    notif_type = models.CharField(max_length=30, choices=NOTIF_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class WebPushToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="webpush_tokens")
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


