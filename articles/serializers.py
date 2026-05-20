from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(read_only=True, source='author')

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'author_id',
            'image',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 'updated_at']
