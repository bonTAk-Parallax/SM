from django.shortcuts import render
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin
from rest_framework import generics

User = get_user_model()

class NotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    


