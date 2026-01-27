from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Prefetch
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    REQUIRED_FIELDS = ["email", "age"]

    def __str__(self):
        return self.username 
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pic = models.ImageField(upload_to="profile_pics/", default="profile_pics/default-profile-pic.webp")
    caption = models.CharField(max_length=200, blank=True)
    # following = models.ManyToManyField(User, through="Following_thru")
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="Following_thru",
        related_name="followers"
    )
    # Add numbers of posts of a user after creating a Posts model
    # user isn't able to follow themselves - can manage through UI


    # @property
    # def followers(self):
    #     prefetch = Prefetch(Profile, following__exact = self.user)
    #     return len([follower for follower in prefetch])
    @property
    def followers_count(self):
        return self.followers.count()


    def __str__(self):
        return self.user.username
    

# class Following_thru(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Following_thru(models.Model):
    from_profile = models.ForeignKey(Profile, related_name="following_relations", on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name="follower_relations", on_delete=models.CASCADE)


    def clean(self):
        if self.from_profile == self.to_profile:
            raise ValidationError("Users cannot follow themselves")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
