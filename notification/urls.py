from django.urls import path
from . import views

urlpatterns = [
    path("notification/", views.NotificationView.as_view(), name="notification" ),
    path("notification/<int:pk>/", views.NotificationDetailView.as_view(), name="notification-detail"),
]