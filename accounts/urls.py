from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from accounts.auth_views import LoginAPIView, RegisterAPIView
from accounts.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
	path('auth/register/', RegisterAPIView.as_view(), name='auth_register'),
	path('auth/login/', LoginAPIView.as_view(), name='auth_login'),
	path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls