from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, InfluencerViewSet, VideoRequestViewSet

router = DefaultRouter()
router.register(r'influencers', InfluencerViewSet)
router.register(r'video_requests', VideoRequestViewSet)
router.register(r'users', UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
