from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from app_users.models import *
from post.models import *
from django_currentuser.db.models import CurrentUserField
from crum import get_current_user
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

@receiver(post_save, sender=PostLike)
def post_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        Notification.objects.create(
            receiver = post.created_by,
            triggerer = instance.created_by,
            notif_type = f"{instance.created_by} liked your post",
            content_type = ContentType.objects.get_for_model(Post),
            object_id = post.id
        )


@receiver(post_save, sender=Comment)
def post_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        Notification.objects.create(
            receiver = post.created_by,
            triggerer = instance.created_by,
            notif_type = f"{instance.created_by} commented on your post",
            content_type = ContentType.objects.get_for_model(Post),
            object_id = post.id
        )

@receiver(post_save, sender=CommentLike)
def comment_like_notification(sender, instance, created, **kwargs):
    if created:
        comment = instance.comment
        Notification.objects.create(
            receiver = comment.created_by,
            triggerer = instance.created_by,
            notif_type = f"{instance.created_by} liked your comment",
                    content_type = ContentType.objects.get_for_model(Comment),
            object_id = comment.id  
        )

@receiver(post_save, sender=Reply)
def comment_reply_notification(sender, instance, created, **kwargs):
    if created and not instance.parent_reply:
        comment = instance.comment
        Notification.objects.create(
            receiver = comment.created_by,
            triggerer = instance.created_by,
            notif_type = f"{instance.created_by} replied to your comment",
            content_type = ContentType.objects.get_for_model(Comment),
            object_id = comment.id
        )

@receiver(post_save, sender=Reply)
def reply_to_reply_notification(sender, instance, created, **kwargs):
    if created and instance.parent_reply:
        parent_reply = instance.parent_reply
        Notification.objects.create(
            receiver = parent_reply.created_by,
            triggerer = instance.created_by,
            notif_type = f"{instance.created_by} replies to your reply",
            content_type = ContentType.objects.get_for_model(Reply),
            object_id = parent_reply.id
        )
    
@receiver(post_save, sender=ReplyLike)
def reply_like_notification(sender, instance, created, **kwargs):
    if created:
        reply = instance.reply
        Notification.objects.create(
            receiver = reply.created_by,
            triggerer = instance.created_by,
            notif_type = f"{instance.created_by} liked your reply",
            content_type = ContentType.objects.get_for_model(Reply),
            object_id = reply.id
        )

@receiver(post_save, sender=Following_thru)
def follower_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            receiver = instance.to_profile.user,
            triggerer = instance.from_profile.user,
            notif_type = f"{instance.created_by} followed you",
            content_type = ContentType.objects.get_for_model(Profile),
            object_id = instance.to_profile.id
        )

# user only gets notifications where they are the receiver and only they can edit it's is_read field
# user search through icontains filter for posts
# give user only their posts back for their profile
