from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

class UserAccountManager(BaseUserManager):
    """
    Custom manager for creating users. Overwrites Django's default user manager
    """

    def create_user(self, username, password, secret):
        """Create a new User object"""

        user = self.model(
            username=username,
            password=password,
            secret=secret
        )

        # Hash the password and save the User object
        #user.set_password(password)
        
        user.save()

        return user


class AppUser(AbstractBaseUser):
    """
    The custom User model. Overwrites Django's default User model.
    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255, default="")
    secret = models.CharField(max_length=255, default="")

    objects = UserAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "secret"]

class Blog(models.Model):
    """Model for student organizations"""

    title = models.CharField(max_length=50, default="")
    content = models.EmailField(max_length=100, default="")
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True)
