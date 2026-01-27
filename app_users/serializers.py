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


# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     following = FollowingSerializer(many=True, source = "following_relations", read_only=True)
#     followers_count = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Profile
#         fields = ["user", "caption", "following", "followers_count"]

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    following = FollowingSerializer(many=True, source = "following_relations", read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    profile_pic = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["url", "id", "user", "caption", "following", "followers_count", "profile_pic"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "age", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"error":"Passwords do not match"})
        return data
        

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(
            username = validated_data["username"],
            email = validated_data["email"],
            age = validated_data["age"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user