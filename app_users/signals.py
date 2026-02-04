from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_delete, sender=Profile)
# def delete_profile_pic(sender, instance, **kwargs):
#     pic = instance.profile_pic

#     if not pic:
#         return

#     if pic.name == "profile_pics/default-profile-pic.webp":
#         return
    
#     still_used = Profile.objects.filter(profile_pic=pic.name).exists()
#     if still_used:
#         return 

#     pic.delete(save=False)
