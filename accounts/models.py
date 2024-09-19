from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import datetime


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        extra_fields.setdefault('birth', datetime.date.today())
        return self._create_user(username, email, password, **extra_fields)


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
    verification_code = models.CharField(max_length=10, blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(using=using)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username