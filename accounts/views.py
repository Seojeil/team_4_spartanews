from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import User
from .serializers import UserProfileSerializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    ## 프로필 조회
    # permission_classes = [IsAuthenticated]
    def get(self, request, account_id):
        user = get_object_or_404(User, pk=account_id)
        serializer = UserProfileSerializers(user)
        
        return Response(serializer.data)

    