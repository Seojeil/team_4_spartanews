from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
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
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)
    
    # 기사 상세페이지 (로그인 필요 X)
    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        article.hits += 1
        article.save()
        
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 기사 수정 (로그인 기능 이후에 검증로직 추가 예정)
    def put(self, request, article_pk):
        article = self.get_object(article_pk)
        
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 기사 삭제 (로그인 기능 이후에 검증로직 추가 예정)
    def delete(self, request, article_pk):
        article = self.get_object(article_pk)
        
        article.delete()
        return Response({"detail": "게시글이 삭제되었습니다.."}, status=status.HTTP_204_NO_CONTENT)