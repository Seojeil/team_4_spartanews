from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class CommonField(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s'
        )
    content = models.TextField()
    recommendation = models.ManyToManyField(
        User,
        related_name='%(class)s_recommend',
        )
    non_recommendation = models.ManyToManyField(
        User,
        related_name='%(class)s_non_recommend',
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Article(CommonField):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        )
    hits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        'category',
        on_delete=models.CASCADE,
        related_name='articles'
        )
    tags = models.ManyToManyField(
        'tag',
        related_name='products',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Comment(CommonField):
    article = models.ForeignKey(
        to=Article, 
        on_delete=models.CASCADE, 
        related_name="article_comments", 
        blank=True,
        null=True,
        )

