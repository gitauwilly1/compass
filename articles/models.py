from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        REVIEW = 'REVIEW', 'Review'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    featured_image = CloudinaryField('image', blank=True, null=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title