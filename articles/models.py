from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class TimeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Article(TimeStampeModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
        )
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        )
    recommendation = models.ManyToManyField(
        User,
        related_name='recommend_articles',
        )
    non_recommendation = models.ManyToManyField(
        User,
        related_name='non_recommend_articles',
        )
    hits = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        'category',
        on_delete=models.CASCADE,
        related_name='articles'
        )

    def __str__(self):
        return self.title

# 카테고리
class Category(models.Model):
    name = models.CharField(max_length=30, unique = True)

    def __str__(self):
        return self.name


class Comments(TimeStampeModel):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    recommendation = models.ManyToManyField(
        to=User,
        related_name='recommend_comments',
        )
    non_recommendation = models.ManyToManyField(
        to=User,
        related_name='non_recommend_comments',
        )
    article = models.ForeignKey(
        to=Article, 
        on_delete=models.CASCADE, 
        related_name="article_comments", 
        blank=True,
        null=True,
        )

