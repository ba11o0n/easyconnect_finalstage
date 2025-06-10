from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, email, full_name, role, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(email=self.normalize_email(email), full_name=full_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('attendee', 'Attendee'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return self.email
