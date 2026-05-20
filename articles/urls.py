from django.urls import path
from rest_framework.routers import DefaultRouter
from articles.views import ArticleViewSet

router = DefaultRouter()
router.register(r'', ArticleViewSet, basename='articles')

urlpatterns = router.urls
