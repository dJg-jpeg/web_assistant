from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AssistantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'