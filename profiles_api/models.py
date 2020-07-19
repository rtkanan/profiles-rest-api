from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        # This makes the second half of the email lower case always
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        
        user.save(using=self._db) # 'using' helps to support multiple databases

        return user
    
    def create_super_user(self, email, name, password):
        """Create new superuser"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db) # 'using' helps to support multiple databases

        return user


# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Model Manager
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of the user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of the user"""
        return self.name
    
    def __str__(self):
        """Return string representation of the user"""
        return self.email