from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from backend.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"user_status", UserStatusViewSet, basename="user_status")
router.register(r"user_tracker", UserTrackerViewSet, basename="user_tracker")
router.register(r"blog_post_type", BlogPostTypeViewSet, basename="blog_post_type")
router.register(r"blog_post", BlogPostViewSet, basename="blog_post")
router.register(r"notification", NotificationViewSet, basename="notification")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
