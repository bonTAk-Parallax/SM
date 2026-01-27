from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "age"]

class FollowingSerializer(serializers.Serializer):
    class Meta:
        model = Following_thru
        fields = ["from_profile", "to_profile"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    following = FollowingSerializer(many=True, source = "following_relations", read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Profile
        fields = ["user", "caption", "following", "followers_count"]