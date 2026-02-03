from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    age = serializers.IntegerField( read_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "age", "profile_pic"]

    



class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following_thru
        fields = ["to_profile"]



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    following = FollowingSerializer(many=True, source = "following_relations", read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Profile
        fields = ["url", "id", "user", "caption", "following", "following_count", "followers_count", "created_date"]



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    birth_date = serializers.DateField(required=True)
    profile_pic = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "birth_date", "profile_pic", "password", "confirm_password"]

    def validate_birth_date(self, value):
        age = User.calculate_age(value)
        if not 18 <= age <= 100:
            raise serializers.ValidationError(
                "You must be above 18 to use this application"
            )
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"error":"Passwords do not match"})
        return data
        

    def create(self, validated_data):
        profile_pic = validated_data.pop("profile_pic", None)
        validated_data.pop("confirm_password")
        user = User(
            username = validated_data["username"],
            email = validated_data["email"],
            birth_date = validated_data["birth_date"]
        )
        user.set_password(validated_data["password"])
        user.save()
        profile= user.profile
        if profile_pic:
            profile.profile_pic=profile_pic
            profile.save()
        return user
    


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", required = False)
    email = serializers.EmailField(source="user.email", required = False)
    birth_date = serializers.DateField(source="user.birth_date", required = False)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)
    password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = Profile
        fields = [
            'username', 'email', 'birth_date', 'caption', 'profile_pic', 'new_password', 'password'
        ]
        
    def validate(self, data):
        user = self.instance.user
        if check_password(data.get("password"), user.password):
            return data
        raise serializers.ValidationError("Incorrect Password! Cannot update information.")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.birth_date = user_data.get("birth_date", user.birth_date)

        if "new_password" in validated_data:
            user.set_password(validated_data.pop("new_password", None))
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class ConfirmPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        password = attrs.get("password")
        if user.check_password(password):
            return attrs
        raise serializers.ValidationError({"error": "Wrong password, cannot delete"})
    
