from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from . managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the project.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=254)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """
        String representation of the user's full name.
        """
        return f'{self.first_name} {self.last_name}'

    class Meta:
        """
        Meta class for the model.
        """
        verbose_name = 'user'
        verbose_name_plural = 'users'