from django.db import models
from django.contrib.auth import get_user_model


# 주석처리된 부분은 외래키이기 때문에 지금 작성이 안되는 부분입니다.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='articles'
        )
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        )
    # comments = models.ForeignKey()
    recommendation = models.ManyToManyField(
        get_user_model(),
        related_name='recommend_articles',
    )
    non_recommendation = models.ManyToManyField(
        get_user_model(),
        related_name='non_recommend_articles',
    )
    hits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
