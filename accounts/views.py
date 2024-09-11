from rest_framework.views import APIView
from rest_framework.response import Response
from .validators import validate_signup
from .serializers import UserSerializer
from .models import User


class SignupView(APIView):

    # 회원가입
    def post(self, request):
        is_valid, err_msg = validate_signup(request.data)
        if not is_valid:
            return Response({"error": err_msg}, status=400)
        
        user = User.objects.create_user(**request.data)
        
        serializer = UserSerializer(user)
        return Response(serializer.data) 
