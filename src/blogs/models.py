from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    """Model for student organizations"""

    title = models.CharField(max_length=50, default="")
    content = models.EmailField(max_length=100, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
