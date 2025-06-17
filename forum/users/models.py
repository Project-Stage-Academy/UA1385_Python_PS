from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    user_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, default='')
    user_phone = PhoneNumberField(blank=True, default='')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    ROLES = [
        (1, "Investor"),
        (2, "Startup"),
    ]
    roles = ArrayField(
        models.PositiveSmallIntegerField(choices=ROLES),
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'



