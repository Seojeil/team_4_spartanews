from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        )
    
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(
        max_length=50, null=True, blank=True, unique=True)
    birth = models.DateField()
    gender = models.CharField(choices=GENDER, max_length=1, default='O')
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers')
    bio = models.TextField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(using=using)

    @classmethod
    def create_superuser(cls, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # 생일 삭제
        extra_fields.pop('birth', None)

        return cls._create_user(username, email, password, **extra_fields)