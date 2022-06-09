from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.

class AssistantUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    created_at = models.DateField(null=False, auto_now_add=True)
    storage_size = models.IntegerField(default=0)
    storage_limit = models.IntegerField(default=1e+7)
    token_cookie = models.CharField(max_length=254, null=True, default=None)

    REQUIRED_FIELDS = ['username', 'email', 'password']

    def __str__(self):
        return f"User({self.username}, {self.email})"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']


class Contact(models.Model):
    name = models.CharField(max_length=40, null=False)
    birthday = models.DateField(null=False)
    email = models.EmailField(max_length=50, unique=True, null=False)
    address = models.CharField(max_length=50)
    updated_at = models.DateField(null=False, auto_now=True)
    created_at = models.DateField(null=False, auto_now_add=True)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']


class ContactPhone(models.Model):
    phone = models.CharField(max_length=13, unique=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    updated_at = models.DateField(null=False, auto_now=True)
    
    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'
        ordering = ['-updated_at']


class Note(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=False)
    done = models.BooleanField(default=False)
    updated_at = models.DateField(null=False, auto_now=True)
    created_at = models.DateField(null=False, auto_now_add=True)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-done']


class NoteTag(models.Model):
    tag = models.CharField(max_length=20)
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    updated_at = models.DateField(null=False, auto_now=True)
    
    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['-updated_at']
    