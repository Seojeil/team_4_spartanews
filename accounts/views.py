from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import User
from .serializers import UserProfileSerializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .validators import validate_signup


class SignupView(APIView):
    # 회원가입
    def post(self, request):
        is_valid, err_msg = validate_signup(request.data)
        if not is_valid:
            return Response({"error": err_msg}, status=400)

        user = User.objects.create_user(**request.data)

        serializer = UserProfileSerializers(user)
        return Response(serializer.data)


class UserProfileView(APIView):
    # 프로필 조회
    # permission_classes = [IsAuthenticated]
    def get(self, request, account_id):
        user = get_object_or_404(User, pk=account_id)
        serializer = UserProfileSerializers(user)

        return Response(serializer.data)
