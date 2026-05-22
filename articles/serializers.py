from rest_framework import serializers
from articles.models import Article, Category, Comment, Bookmark

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.full_name',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'article',
            'author',
            'author_name',
            'body',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'author',
            'article',
            'author_name',
            'created_at',
            'updated_at',
        ]

class ArticleSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(
        source='author.full_name',
        read_only=True
    )

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField( read_only=True)
    likes_count = serializers.IntegerField( read_only=True)
    is_liked = serializers.SerializerMethodField()
    bookmarks_count = serializers.IntegerField(read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Article

        fields = [
            'id',
            'author',
            'author_name',
            'category',
            'category_name',
            'title',
            'slug',
            'featured_image',
            'excerpt',
            'content',
            'view_count',
            'is_featured',
            'status',
            'published_at',
            'comments',
            'comments_count',
            'likes_count',
            'bookmarks_count',
            'is_bookmarked',
            'is_liked',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'author',
            'view_count',
            'published_at',
            'created_at',
            'updated_at',
            'comments',
            'comments_count',
            'likes_count',
            'bookmarks_count',
            'is_bookmarked',
            'is_liked',
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return obj.is_liked_by(request.user)

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return obj.is_bookmarked_by(request.user)
