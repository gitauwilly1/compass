from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField   

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        REVIEW = 'review', 'In Review'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
        
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    featured_image = CloudinaryField('image', blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    content = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def likes_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        if user is None or not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    @property
    def bookmarks_count(self):
        return self.bookmarks.count()

    def is_bookmarked_by(self, user):
        if user is None or not user.is_authenticated:
            return False
        return self.bookmarks.filter(user=user).exists()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.email} on {self.article.title}"


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Like by {self.user.email} on {self.article.title}"


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Bookmark by {self.user.email} on {self.article.title}"
