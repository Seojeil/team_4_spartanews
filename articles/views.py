from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Article, Category, Comment
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    CommentSerializer
    )


class ArticleAPIView(APIView):
    # 모든 기사 조회
    def get(self, request):
        data_type = request.data.get("data_type") # articles/comments
        sort_type = request.data.get("sort_type") # recommendation/created_at/hits(articles일때만)
        
        # 댓글조회/정렬
        if data_type == 'comments':
            # 추천순 정렬
            if sort_type == 'recommendation':
                comments = Comment.objects.annotate(
                    recommendation_count=Count('recommendation')-Count('non_recommendation')
                    ).order_by('-recommendation_count', '-created_at')
            # 작성순 정렬
            else:
                comments = Comment.objects.all().order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
        # 기사조회/정렬
        else:
            # 추천순 정렬
            if sort_type == 'recommendation':
                articles = Article.objects.annotate(
                    recommendation_count=Count('recommendation')-Count('non_recommendation')
                    ).order_by('-recommendation_count', '-created_at')
            # 조회수순 정렬
            elif sort_type == 'hits':
                articles = Article.objects.all().order_by('-hits', '-created_at')
            #작성순 정렬
            else:
                articles = Article.objects.all().order_by('-created_at')
            serializer = ArticleSerializer(articles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 기사 작성
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        category_id = request.data.get('category')
        category = get_object_or_404(Category, id=category_id)
        
        serializer = ArticleSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, category=category)
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


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)
    
    # 댓글 작성
    def post(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, article = article)
            
            return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)
    
    # 댓글 추천, 비추천
    def post(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        # 추천
        if request.data.get('evaluate') == 'recommendation':
            comment.non_recommendation.remove(request.user)
            if comment.recommendation.filter(pk=request.user.pk).exists():
                comment.recommendation.remove(request.user)
                return Response({"detail": "추천이 취소되었습니다."}, status=status.HTTP_200_OK)
            else:
                comment.recommendation.add(request.user)
                comment.save()
                return Response({"detail": "이 댓글을 추천합니다."}, status=status.HTTP_200_OK)
        # 비추천
        else:
            comment.recommendation.remove(request.user)
            if comment.non_recommendation.filter(pk=request.user.pk).exists():
                comment.non_recommendation.remove(request.user)
                return Response({"detail": "비추천이 취소되었습니다."}, status=status.HTTP_200_OK)
            else:
                comment.non_recommendation.add(request.user)
                comment.save()
                return Response({"detail": "이 댓글을 비추천합니다."}, status=status.HTTP_200_OK)
    
        # 댓글 수정
    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(instance = comment, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_at=timezone.now())
            return Response(serializer.data)
    
        # 댓글 삭제 기능
    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        if comment.author != request.user:
            return Response({"message":"삭제할 권한이 없습니다"})
        comment.delete()
        return Response({"message":"댓글을 성공적으로 삭제했습니다"})
    

