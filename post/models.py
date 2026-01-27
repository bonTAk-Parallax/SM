from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# Create your models here.

class Posts(models.Model):
    text_content = models.TextField(max_length=300, blank=True)
    image_content = models.ImageField(upload_to="post_pics/", blank=True)
    post_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post_like")
    
    def clean(self):
        if self.text_content and self.image_content is None:
            raise ValidationError("You must have some texts or an image for it to be posted!")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="posts")
    post_reply = models.TextField(max_length=150, blank=False)
    comment_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment_like")


class CommentReply(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    comment_reply = models.TextField(max_length=50, blank=False)
    reply_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reply_like")
