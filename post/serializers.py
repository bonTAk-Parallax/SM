from rest_framework import serializers
from app_users.serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from .models import *
from app_users.views import *

User = get_user_model()

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ProfilePostSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['profile_pic']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="posted_by.user.username", read_only=True)
    profile_pic = serializers.ImageField(source="posted_by.profile_pic", read_only=True)
    post_like_method = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'username', 'profile_pic', 'text_content', 'image_content', 'post_like_method', 'posted_date']

    def validate(self, data):
        if not data.get("text_content", "").strip() and not data.get("image_content", None):
            raise serializers.ValidationError({"error": "You must have some text or an image for it to be posted!"})
        return data
    

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="commented_by.user.username", read_only=True)
    profile_pic = serializers.ImageField(source="commented_by.profile_pic", read_only=True)
    post = serializers.IntegerField(source="post.id", read_only=True)
    comment_like_method = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['post', 'id', 'username', 'profile_pic', 'comment_content', 'comment_like_method', 'commented_date']

    def validate(self, data):
        if not data.get("comment_content", "").strip():
            raise serializers.ValidationError({"error": "cannot comment empty fields"})
        return data
    


class ReplySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="replied_by.user.username", read_only=True)
    profile_pic = serializers.ImageField(source="replied_by.profile_pic", read_only=True)
    comment = serializers.IntegerField(source='comment.id', read_only=True)
    reply_like_method = serializers.IntegerField(read_only=True)
    parent_reply = serializers.IntegerField(source="parent_reply.id", read_only=True)

    class Meta:
        model = Reply
        fields = ['comment', 'parent_reply', 'id', 'username', 'profile_pic', 'reply_content', 'reply_like_method', 'replied_date']

    def validate(self, data):
        if not data.get("reply_content", "").strip():
            raise serializers.ValidationError({"errors": "cannot post empty reply"})
        return data