from rest_framework import serializers
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("author", "recommendation", "non_recommendation")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("author", "recommendation", "non_recommendation","article",)


class ArticleDetailSerializer(ArticleSerializer):
    article_comments = CommentSerializer(many=True, read_only=True)
    