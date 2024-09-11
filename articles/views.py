from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticletSerializer


# 로그인한 사용자의 경우에만 접근할 수 있도록 수정예정, 아직 로그인기능이 없습니다.
class ArticleAPIView(APIView):
    def post(self, request):
        serializer = ArticletSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)