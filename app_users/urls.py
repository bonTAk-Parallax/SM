from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})

# urlpatterns = [
#     path("profiles/", profile_list, name="profile-list"),
#     path("profile/<int:pk>", profile_detail, name="profile-detail")
# ]

router = DefaultRouter()
router.register(r"profiles", views.ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name = "user-register"),
    path("profiles/edit", ProfileUpdateView.as_view(), name = "profile-udpate"),
    path('profile/delete/', DeleteProfileView.as_view(), name="profile-delete")
]