from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from app_users.models import *
from abc import ABC, abstractmethod

User = get_user_model()

class BaseModel(models.Model):
    made_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="%(class)s_made_by", null=True, blank=True)
    made_at = models.DateTimeField(auto_now_add = True)
    modified_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="%(class)s_modified_by", null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modification_history = models.JSONField(default=list, blank=True)

    class Meta:
        abstract = True

    def capture_history(self):
        history = self.modification_history or []
        history.append({
            "modified_by": self.modified_by.user.username if self.modified_by else None,
            "modified_at": self.modified_at.isoformat(),
        })
        self.modification_history = history

class Post(BaseModel):
    text_content = models.TextField(validators = [MaxLengthValidator(300)], blank=True)
    image_content = models.ImageField(upload_to="post_pics/", blank=True)
    like = models.ManyToManyField(Profile, through="PostLike", related_name="liked_post", blank=True)
    # posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posted')
    # posted_date = models.DateTimeField(auto_now_add=True)

    @property
    def post_like_method(self):
        return self.like.count()


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