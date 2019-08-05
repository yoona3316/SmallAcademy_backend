from django.db import models

# Create your models here.

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, realname, password, email, is_teacher=False, profile=''):
        user = self.model(
            username = username,
            realname = realname,
            email = self.normalize_email(email),
            is_teacher = is_teacher,
            profile = profile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(
            username = username,
            realname='관리자',
            password = password,
            email = email,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    realname = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    is_teacher = models.BooleanField(default=False)
    profile = models.CharField(max_length=80, null=True, blank=True)
    active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
