from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articles.models import Article
from articles.permissions import IsAuthorOrHasRole
from articles.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().select_related('author')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrHasRole]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        status = self.request.query_params.get('is_published')
        author_id = self.request.query_params.get('author_id')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(author__email__icontains=q)
                | Q(author__first_name__icontains=q)
                | Q(author__last_name__icontains=q)
            )

        if status is not None:
            if status.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(is_published=True)
            elif status.lower() in ['false', '0', 'no']:
                queryset = queryset.filter(is_published=False)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-articles', permission_classes=[IsAuthenticated])
    def my_articles(self, request):
        articles = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='drafts', permission_classes=[IsAuthenticated])
    def drafts(self, request):
        if request.user.role in ['editor', 'admin', 'superadmin']:
            articles = self.get_queryset().filter(is_published=False)
        else:
            articles = self.get_queryset().filter(author=request.user, is_published=False)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-author')
    def by_author(self, request):
        author_id = request.query_params.get('author_id')
        if not author_id:
            return Response({'detail': 'author_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        articles = self.get_queryset().filter(author_id=author_id)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stats', permission_classes=[IsAuthenticated])
    def stats(self, request):
        queryset = self.get_queryset()
        total = queryset.count()
        published = queryset.filter(is_published=True).count()
        drafts = queryset.filter(is_published=False).count()
        return Response({'total': total, 'published': published, 'drafts': drafts})

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        article = self.get_object()
        article.is_published = True
        article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        article = self.get_object()
        article.is_published = False
        article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data)
