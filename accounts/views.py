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
from .utils import email_verification_code, send_verification_email


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

        verification_code = email_verification_code()
        
        user_data = request.data.copy()
        user_data['is_active'] = False
        user_data['verification_code'] = verification_code
        user = User.objects.create_user(**user_data)
        
        send_verification_email(user.email, verification_code)

        serializer = UserProfileSerializers(user)
        return Response({"message": "회원가입이 완료되었습니다. 이메일을 확인해주세요",
                         "user": serializer.data}, status = status.HTTP_201_CREATED)
        
    # 회원 비활성화
    def delete(self, request):
        user = request.user
        password = request.data.get("password")

        if user.check_password(password):
            user.delete()
            return Response({"message": "회원 비활성화"})
        else:
            return Response({"message": "비밀번호가 일치하지않습니다."}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        try:
            user = User.objects.get(email=email, verification_code=verification_code)
            if not user.is_active:
                user.is_active = True
                user.verification_code = None
                user.save()
                return Response({"message": "이메일 인증이 완료되었습니다."})
            else:
                return Response({"message":"이미 인증된 계정입니다."}, status = status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message":"잘못된 이메일 또는 인증 코드입니다."}, status = status.HTTP_400_BAD_REQUEST)

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

    # 비밀번호 변경
    def put(self, request):
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
