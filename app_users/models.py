from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(default=date(date.today().year - 18, date.today().month, date.today().day))
    profile_pic = models.ImageField(upload_to="profile_pics/", default="profile_pics/default-profile-pic.webp", blank=True, null=True)
    # age = models.PositiveIntegerField()
    REQUIRED_FIELDS = ["email", "birth_date"]

    @staticmethod
    def calculate_age(birth_date):
        today = date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    
    @property
    def age(self):
        return self.calculate_age(self.birth_date)

    def __str__(self):
        return self.username 
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, blank=True)
    # following = models.ManyToManyField(User, through="Following_thru")
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="Following_thru",
        related_name="followers"
    )
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # Add numbers of posts of a user after creating a Posts model
    # user isn't able to follow themselves - can manage through UI


    # @property
    # def followers(self):
    #     prefetch = Prefetch(Profile, following__exact = self.user)
    #     return len([follower for follower in prefetch])
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()


    def __str__(self):
        return self.user.username
    

# class Following_thru(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Following_thru(models.Model):
    from_profile = models.ForeignKey(Profile, related_name="following_relations", on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name="follower_relations", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["from_profile", "to_profile"],
                name = "unique_follow"
            )
        ]


    def clean(self):
        if self.from_profile == self.to_profile:
            raise ValidationError("Users cannot follow themselves")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
