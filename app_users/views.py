from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Create your views here.

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

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

