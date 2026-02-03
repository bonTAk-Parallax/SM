from rest_framework import serializers
from app_users.serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from .models import *
from app_users.views import *

User = get_user_model()

# Serializer that accepts dynamically modifying fields, task for tomorrow: https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
# Real Time notification system; mentions, JS problem solving (2-3) and functions familiarity through DOM, vue theory
# palindrome, armstrong, sort/order, binary search, factorial, fibonacci(recursive too), number guess game
class BaseSerializer(serializers.Serializer):
    username = serializers.CharField(source="created_by.username", read_only=True)
    profile_pic = serializers.ImageField(source="created_by.profile_pic", read_only=True)
    

class PostSerializer(BaseSerializer, serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)
    text_content = serializers.RegexField(
         regex=r'^[a-zA-Z]$',
         error_messages = {
             'invalid': 'Text Content can only contain text',
             'required': 'Text Content is required'
         })         #Learning only, need to delete later on
    class Meta:
        model = Post
        fields = ['id', 'username', 'profile_pic', 'text_content', 'image_content', 'total_likes', 'created_at','modification_history']
        read_only_fields=['modification_history']
    

    def get_total_likes(self, obj):
        return obj.post_like_method

    def validate(self, attrs):
        text = attrs.get("text_content")
        image = attrs.get("image_content")
        if not text and not image:
            raise serializers.ValidationError({
                "none_fields_error": "You must have some text or an image for it to be posted!"
            })

        return attrs


class CommentSerializer(BaseSerializer, serializers.ModelSerializer):
    post = serializers.IntegerField(source="post.id", read_only=True)
    comment_like_method = serializers.IntegerField(read_only=True)
    modification_history = serializers.JSONField(read_only=True)

    class Meta:
        model = Comment
        fields = ['post', 'id', 'username', 'profile_pic', 'comment_content', 'comment_like_method', 'created_at', 'modification_history' ]

    def validate(self, data):
        if not data.get("comment_content", "").strip():
            raise serializers.ValidationError({"error": "cannot comment empty fields"})
        return data
    


class ReplySerializer(BaseSerializer, serializers.ModelSerializer):
    comment = serializers.IntegerField(source='comment.id', read_only=True)
    reply_like_method = serializers.IntegerField(read_only=True)
    parent_reply = serializers.IntegerField(source="parent_reply.id", read_only=True)
    modification_history = serializers.JSONField(read_only=True)

    class Meta:
        model = Reply
        fields = ['comment', 'parent_reply', 'id', 'username', 'profile_pic', 'reply_content', 'reply_like_method', 'created_at', 'modification_history']

    def validate(self, data):
        if not data.get("reply_content", "").strip():
            raise serializers.ValidationError({"errors": "cannot post empty reply"})
        return data