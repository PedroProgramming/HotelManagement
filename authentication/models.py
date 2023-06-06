from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class Users(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=200, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = UserManager()

    zip_code = models.CharField(max_length=9, blank=True)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=25)
    neighborhood = models.CharField(max_length=20)
    cell_phone = models.CharField(max_length=11)
    telephone = models.CharField(max_length=11, blank=True, null=True)
    recovery_email = models.EmailField()


    def __str__(self):
        return self.email