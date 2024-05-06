from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserAccountManager(BaseUserManager):
    """
    Custom manager for creating users. Overwrites Django's default user manager
    """

    def create_superuser(self, username, password, email, secret, **other_fields):
        """
        Create a superuser. Overwrites Django's default function.
        """

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("The is_staff field must be True for superusers."))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("The is_superuser field must be True for superusers."))
        
        return self.create_user(username, password, email, secret, **other_fields)


    def create_user(self, username, password, email, secret, **other_fields):
        """Create a new User object"""

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            password=password,
            email=email, 
            secret=secret,
            **other_fields
        )

        # Hash the password and save the User object
        user.set_password(password)

        user.save()

        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    """
    The custom User model. Overwrites Django's default User model.
    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="", unique=True)
    secret = models.CharField(max_length=255, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "secret"]

class Blog(models.Model):
    """Model for student organizations"""

    title = models.CharField(max_length=50, default="")
    content = models.EmailField(max_length=100, default="")
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
