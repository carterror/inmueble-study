from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Create your models here.

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=None, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#
# class MyAccount(BaseUserManager):
#     def create_user(self, first_name, last_name, email, username, phone,password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email is required')
#
#         if not username:
#             raise ValueError('Username is required')
#
#         if not phone:
#             raise ValueError('Phone is required')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             phone=phone,
#             username=username
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, first_name, last_name, email, username, phone, password=None, **extra_fields):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             username=username,
#             phone=phone,
#             password=password
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
#
#
# class Account(AbstractBaseUser):
#     first_name = models.CharField(max_length=50, null=True)
#     last_name = models.CharField(max_length=50, null=True)
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=100, unique=True)
#     phone = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superadmin = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now_add=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['phone', 'password', 'username', 'first_name', 'last_name']
#
#     objects = MyAccount()
#
#     def __str__(self):
#         return self.email
#
#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True
