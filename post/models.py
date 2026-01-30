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

    @property
    def post_like_method(self):
        return self.likes.count()


class PostLike(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["made_by", "post"],
                name = "unique_user_post_like"
            )
        ]


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment_content = models.TextField(validators = [MaxLengthValidator(150)], blank=False)

    @property
    def comment_like_method(self):
        return self.comment_likes.count()


class CommentLike(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["made_by", "comment"],
                name = "unique_user_comment_like"
            )
        ]


class Reply(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    parent_reply = models.ForeignKey("self", on_delete=models.CASCADE, related_name="child_replies", null=True, blank=True)
    reply_content = models.TextField(validators = [MaxLengthValidator(50)], blank=False)

    @property
    def reply_like_method(self):
        return self.reply_likes.count()


class ReplyLike(BaseModel):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='reply_likes')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["made_by", "reply"],
                name = "unique_user_reply_like"
            )
        ]