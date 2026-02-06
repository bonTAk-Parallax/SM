import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from notification.tasks import process_mentions

MENTION_REGEX = r'@(\w+)'

@receiver(post_save, sender=Comment)
@receiver(post_save, sender=Post)
@receiver(post_save, sender=Reply)
def mention_notification(sender, instance, created, **kwargs):
    if not created:
        return
    text = instance.text_content
    usernames = set(re.findall(MENTION_REGEX, text))
    if usernames:
        process_mentions.delay(
            usernames=list(usernames),
            triggerer = instance.created_by,
        )
    
