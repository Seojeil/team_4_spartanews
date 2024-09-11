from rest_framework import serializers
from .models import Article


class ArticletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'hits', 'created_at', 'updated_at']
        # read_only_fields = ()