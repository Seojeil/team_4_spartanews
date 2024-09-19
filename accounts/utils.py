import random
import string
from django.core.mail import send_mail

def email_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_email(email, verification_code):
    subject = '이메일 인증'
    message = f'회원가입을 완료하려면 다음 인증 코드를 입력하세요: {verification_code}'
    from_email = 'kgmin94@naver.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)