from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView

# Create your views here.

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all().order_by('-created_date')
    serializer_class = ProfileSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if username:
            temp = Profile.objects.filter(user__username__icontains = username)
            if temp:
                return temp
        return Profile.objects.all()

    @action(detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def follow(self, request, pk=None):
        target_profile = self.get_object()
        from_profile = request.user.profile

        if from_profile == target_profile:
            return Response(
                {"detail": "You cannot follow yourself!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow, created = Following_thru.objects.get_or_create(
            from_profile=from_profile,
            to_profile = target_profile
        )
        if not created:
            return Response(
                {"detail":"Already following"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            "detail": f"You are now following {target_profile.user.username}"
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['posts'], permission_classes = [IsAuthenticated])
    def unfollow(self, request, pk=None):
        target_profile = self.get_object()
        from_profile = requeset.user.profile

        deleted, = Following_thru.objects.filter(
            from_profile = from_profile,
            to_profile = target_profile
        ).delete()

        if deleted == 0:
            return Reponse(
                {"detail": f"You aren't following {target_profile}"},
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"detail": f"You unfollowed {target_profile}"},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        profile = self.get_object()
        followers = Profile.objects.filter(following_relations__to_profile = profile)
        serializer = ProfileSerializer(followers, many=True, context={"request": request})
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        profile = self.get_object()
        following = Profile.objects.filter(following_relations__from_profile = profile)
        serializer = ProfileSerializer(following, many=True, context={"request": request})
        return Response(serializer.data)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = serializer.instance
        profile = user.profile
        profile_serializer = ProfileSerializer(profile, context = {"request": request})
        return Response(
            {
                "message": "User successfully created!",
                "Profile": profile_serializer.data,
            },
            status = status.HTTP_201_CREATED,
            headers = headers
        )
    

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user.profile
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": f"Profile for user: {self.get_object()} has been successfully updated!",
                "Profile": serializer.data
            }, 
            status = status.HTTP_200_OK
        )
    

class DeleteProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmPasswordSerializer

    def get_object(self):
        return self.request.user


    def post(self, request):
        
        serializer = self.get_serializer(
            data = request.data,
            context = {"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        #user.is_active = False for temprorary deactivation
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
