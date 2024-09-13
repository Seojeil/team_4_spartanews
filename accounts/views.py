from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .validators import validate_signup
from .models import User
from .serializers import (
    UserProfileSerializers,
    UserUpdateSerializers,
    UserChangePasswordSerailizers
)


class SignupView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    # 회원가입
    def post(self, request):
        is_valid, err_msg = validate_signup(request.data)
        if not is_valid:
            return Response({"error": err_msg}, status=400)

        user = User.objects.create_user(**request.data)

        serializer = UserProfileSerializers(user)
        return Response(serializer.data)

    # 회원 비활성화
    def delete(self, request):
        user = request.user
        password = request.data.get("password")

        if user.check_password(password):
            user.delete()
            return Response({"message": "회원 비활성화"})
        else:
            return Response({"message": "비밀번호가 일치하지않습니다."}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, account_id):
        return get_object_or_404(User, pk=account_id)

    # 프로필 조회
    def get(self, request, account_id):
        user = self.get_object(account_id)
        serializer = UserProfileSerializers(user)
        return Response(serializer.data)

    # 팔로우
    def post(self, request, account_id):
        user = self.get_object(account_id)

        if user == request.user:
            return Response({"error": "자신을 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            return Response({"detail": "팔로우가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            user.followers.add(request.user)
            return Response({"detail": "팔로우되었습니다."}, status=status.HTTP_200_OK)

    # 프로필 수정
    def put(self, request, account_id):
        # 1. 특정 회원정보
        user = request.user

        if user.id != account_id:
            return Response({"message": "회원 정보와 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = UserUpdateSerializers(
            instance=user, data=request.data, partial=True)

        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # 비밀번호 변경
        if request.data.get("prev_password") == request.data.get("password_1"):
            return Response({"message": "기존의 비밀번호와 일치합니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserChangePasswordSerailizers(
            instance=request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "비밀번호변경완료"})


class UserLoginView(APIView):
    # 회원 로그인
    # 1. 아이디와 비밀번호 검사
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            allowed_id = {
                "user_id": user.id,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(allowed_id)

        else:
            return Response({"message": "아이디 또는 비밀번호가 일치하지않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # 회원 로그아웃
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
