from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from app_users.models import *

User = get_user_model()

class Post(models.Model):
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posted')
    text_content = models.TextField(validators = [MaxLengthValidator(300)], blank=True)
    image_content = models.ImageField(upload_to="post_pics/", blank=True)
    like = models.ManyToManyField(Profile, through="PostLike", related_name="liked_post", blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)

    @property
    def post_like_method(self):
        # return len([count for count in self.like])
        return self.like.count()
    
    # def clean(self):
    #     if not self.text_content and not self.image_content:    
    #         raise ValidationError("You must have some texts or an image for it to be posted!")

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     return super().save(*args, **kwargs)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_liked_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_liked')
    post_like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post_liked_by", "post"],
                name = "unique_user_post_like"
            )
        ]


class Comment(models.Model):
    commented_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='commented')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment_content = models.TextField(validators = [MaxLengthValidator(150)], blank=False)
    comment_like = models.ManyToManyField(Profile, through="CommentLike", related_name="liked_comment", blank=True)
    commented_date = models.DateTimeField(auto_now_add=True)

    @property
    def comment_like_method(self):
        # return len([count for count in self.comment_like])
        return self.comment_like.count()


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    comment_liked_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_liked')
    comment_like_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["comment_liked_by", "comment"],
                name = "unique_user_comment_like"
            )
        ]


class Reply(models.Model):
    replied_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="replied")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    parent_reply = models.ForeignKey("self", on_delete=models.CASCADE, related_name="child_replies", null=True, blank=True)
    reply_content = models.TextField(validators = [MaxLengthValidator(50)], blank=False)
    reply_like = models.ManyToManyField(Profile, through="ReplyLike", related_name="liked_reply", blank=True)
    replied_date = models.DateTimeField(auto_now_add=True)

    @property
    def reply_like_method(self):
        # return len([count for count in self.reply_like])
        return self.reply_like.count()


class ReplyLike(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    reply_liked_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reply_liked")
    reply_like_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reply_liked_by", "reply"],
                name = "unique_user_reply_like"
            )
        ]