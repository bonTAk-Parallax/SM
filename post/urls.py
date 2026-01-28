from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_nested import routers

app_name = "posts"

router = DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="post")
posts_router = routers.NestedDefaultRouter(router, f'posts', lookup='post')
posts_router.register(r"comments", views.CommentViewSet, basename = "post-comments")

comment_router = routers.NestedDefaultRouter(posts_router, r'comments', lookup = 'comment')
comment_router.register(f'replies', views.ReplyViewSet, basename = "comment-replies")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
    path("", include(comment_router.urls))
]