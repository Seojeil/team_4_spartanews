from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserProfileSerializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class UserProfileView(APIView):
    ## 프로필 조회
    # permission_classes = [IsAuthenticated]
    def get(self, request, account_id):
        user = get_object_or_404(User, pk=account_id)
        serializer = UserProfileSerializers(user)
        
        return Response(serializer.data)

    ## 회원 비활성화
    def delete(self, request):
        user = request.user
        user.delete()
        
class UserLoginView(APIView):
    ## 회원 로그인
    ## 1. 아이디와 비밀번호 검사
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            allowed_id = {
                "user_id": user.id,
                'refresh' : str(refresh),
                'access' : str(refresh.access_token)
            }
            
            return Response(allowed_id)
        else:
            return Response({"message":"아이디 또는 비밀번호가 일치하지않습니다."}, status = status.HTTP_400_BAD_REQUEST)