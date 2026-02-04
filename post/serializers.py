from rest_framework import serializers
from app_users.serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from .models import *
from app_users.views import *

User = get_user_model()

# JS problem solving (2-3) and functions familiarity through DOM, vue theory
# palindrome, armstrong, sort/order, binary search, factorial, fibonacci(recursive too), number guess game


# https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)    
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class UserOfPost(UserSerializer, DynamicFieldsModelSerializer):
    pass

class PostSerializer(serializers.ModelSerializer):
    created_by = UserOfPost(fields=['username', 'profile_pic'], read_only=True)
    total_likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'text_content', 'image_content', 'total_likes', 'created_at','modification_history']
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


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserOfPost(fields=['username', 'profile_pic'], read_only=True)
    post = serializers.IntegerField(source="post.id", read_only=True)
    comment_like_method = serializers.IntegerField(read_only=True)
    modification_history = serializers.JSONField(read_only=True)

    class Meta:
        model = Comment
        fields = ['post', 'id', 'created_by', 'comment_content', 'comment_like_method', 'created_at', 'modification_history' ]

    def validate(self, data):
        if not data.get("comment_content", "").strip():
            raise serializers.ValidationError({"error": "cannot comment empty fields"})
        return data
    


class ReplySerializer(serializers.ModelSerializer):
    created_by = UserOfPost(fields=['username', 'profile_pic'], read_only=True)
    comment = serializers.IntegerField(source='comment.id', read_only=True)
    reply_like_method = serializers.IntegerField(read_only=True)
    parent_reply = serializers.IntegerField(source="parent_reply.id", read_only=True)
    modification_history = serializers.JSONField(read_only=True)

    class Meta:
        model = Reply
        fields = ['comment', 'parent_reply', 'id', 'created_by', 'reply_content', 'reply_like_method', 'created_at', 'modification_history']

    def validate(self, data):
        if not data.get("reply_content", "").strip():
            raise serializers.ValidationError({"errors": "cannot post empty reply"})
        return data