from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-posted_date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user.profile)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-commented_date')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post_id=post_pk).order_by('-commented_date')
        return Comment.objects.all().order_by('-commented_date')

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_pk'))
        serializer.save(commented_by=self.request.user.profile, post = post)


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all().order_by('-replied_date')
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        comment_pk = self.kwargs.get('comment_pk')
        if comment_pk:
            return Reply.objects.filter(comment_id=comment_pk).order_by('-replied_date')
        return Reply.objects.all().order_by('-replied_date')

    def perform_create(self, serializer):
        comment = Comment.objects.get(pk=self.kwargs.get('comment_pk'))
        serializer.save(replied_by=self.request.user.profile, comment=comment)
