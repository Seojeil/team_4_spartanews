from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gender = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    birth = models.DateField()
    gender = models.CharField(choices=gender, max_length=1, other='O')
    bio = models.TextField(null=True, blank=True)
    

