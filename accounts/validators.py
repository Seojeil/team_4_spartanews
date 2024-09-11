from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


def validate_signup(signup_data):
    username = signup_data.get('username')
    email = signup_data.get('email')
    password = signup_data.get('password')

    err_msg = []
    
    # 유저네임 검증
    if User.objects.filter(username=username).exists():
        err_msg.append("이미 존재하는 유저네임입니다")
        
    # 이메일 검증
    try:
        validate_email(email)
    except:
        err_msg.append("이메일 형식이 옮바르지 않습니다")

    # 비밀번호 검증
    try:
        validate_password(password)
    except ValidationError as e:
        err_msg.extend(e.messages)
    
    if err_msg:
        return False, err_msg
    else:
        return True, None
