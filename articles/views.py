from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Article
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer
    )


class ArticleAPIView(APIView):
    # 모든 기사 조회
    def get(self, request):
        articles = Article.objects.all()
        
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 기사 작성
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)
    
    # 기사 상세페이지 조회
    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        article.hits += 1
        article.save()
        
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 기사 추천, 비추천
    def post(self, request, article_pk):
        article = self.get_object(article_pk)
        
        # 추천
        if request.data.get('evaluate') == 'recommendation':
            article.non_recommendation.remove(request.user)
            if article.recommendation.filter(pk=request.user.pk).exists():
                article.recommendation.remove(request.user)
                return Response({"detail": "추천이 취소되었습니다."}, status=status.HTTP_200_OK)
            else:
                article.recommendation.add(request.user)
                article.save()
                return Response({"detail": "이 기사를 추천합니다."}, status=status.HTTP_200_OK)
        # 비추천
        else:
            article.recommendation.remove(request.user)
            if article.non_recommendation.filter(pk=request.user.pk).exists():
                article.non_recommendation.remove(request.user)
                return Response({"detail": "비추천이 취소되었습니다."}, status=status.HTTP_200_OK)
            else:
                article.non_recommendation.add(request.user)
                article.save()
                return Response({"detail": "이 기사를 비추천합니다."}, status=status.HTTP_200_OK)
    
    # 기사 수정
    def put(self, request, article_pk):
        article = self.get_object(article_pk)
        
        if article.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 기사 삭제
    def delete(self, request, article_pk):
        article = self.get_object(article_pk)
        
        if article.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        article.delete()
        return Response({"detail": "게시글이 삭제되었습니다.."}, status=status.HTTP_204_NO_CONTENT)