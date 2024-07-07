from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .utils import UserRoles


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email является обязательным')
        if not password:
            raise ValueError('Password является обязательным')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Email является обязательным')
        if not password:
            raise ValueError('Password является обязательным')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)
    role = models.CharField(max_length=20, choices=UserRoles.choices())
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AppUserManager()

    def __str__(self):
        return self.full_name
