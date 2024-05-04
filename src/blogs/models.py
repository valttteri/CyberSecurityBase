from django.db import models

class Blog(models.Model):
    """Model for student organizations"""

    title = models.CharField(max_length=50, default="")
    content = models.EmailField(max_length=100, default="")
