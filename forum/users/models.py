from django.db import models

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
    role = models.PositiveSmallIntegerField(
        choices=[
            (1, "Investor"),
            (2, "Startup"),
        ],
        default=1,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'

class Investor(models.Model):
    investor_id = models.AutoField(primary_key=True)  
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, null=True)
    required_funding = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'investor'
        verbose_name_plural = 'investors'
        db_table = 'investors'

class Startup(models.Model):
    startup_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'startup'
        verbose_name_plural = 'startups'
        db_table = 'startups'