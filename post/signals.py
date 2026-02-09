import re
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import *
from notification.tasks import process_mentions
from notification.models import*

MENTION_REGEX = r'@(\w+)'

@receiver(post_save, sender=Post)
@receiver(post_save, sender=Reply)
@receiver(post_save, sender=Comment)
def mention_notification(sender, instance, created, **kwargs):
    print("Post signal ACTIVATED!!!")
    if not created:
        return
    text = instance.comment_content
    usernames = set(re.findall(MENTION_REGEX, text))
    print(usernames)
    if usernames:
        process_mentions.delay(
            usernames=list(usernames),
            triggerer_id = instance.created_by_id,
        )

@receiver(pre_delete, sender=Post)
@receiver(pre_delete, sender=Reply)
@receiver(pre_delete, sender=Comment)
def mention_notification(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    print(content_type)
    notifications = Notification.objects.filter(content_type = content_type)
    print(notifications)
    if notifications:
        notifications.delete()
    
