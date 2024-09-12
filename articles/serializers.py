from rest_framework import serializers
from .models import Article, Comments


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title','content','image']
        read_only_fields = ("author", "recommendation", "non_recommendation")
        

class ArticleDetailSerializer(ArticleSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["content"]
        read_only_fields = ("author", "recommendation", "non_recommendation","article",)