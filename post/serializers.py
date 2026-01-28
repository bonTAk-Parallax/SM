from rest_framework import serializers
from app_users.serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class PostSerializer(serializers.HyperlinkedModelSerializer):
    posted_by = ProfileSerializer()
    post_like_method = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['posted_by', 'text_content', 'image_content', 'post_like_method']