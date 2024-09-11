from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

        
    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(using=using)