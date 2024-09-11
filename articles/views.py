from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer
    )


# 로그인한 사용자의 경우에만 접근할 수 있도록 수정예정, 아직 로그인기능이 없습니다.
class ArticleAPIView(APIView):
    # 모든 기사 조회 (로그인 필요 X)
    def get(self, request):
        articles = Article.objects.all()
        
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 기사 작성
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ArticleDetailAPIView(APIView):
    # 기사 상세페이지 (로그인 필요 X)
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)