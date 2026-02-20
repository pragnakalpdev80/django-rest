# api/models.py
from django.db import models
import datetime
from django.contrib.auth.models import User

class TimestampedModel(models.Model):
    """Base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True  # Important: makes it abstract


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Book(TimestampedModel):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    description = models.TextField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        # ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Task(TimestampedModel):
    class Priority(models.TextChoices):
        High = "high"
        Medium = "medium"
        Low = "low"
    title = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(choices=Priority,max_length=10)
    due_date = models.DateField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Author(models.Model):
    name = models.CharField(max_length=30)
    bio = models.TextField(max_length=200)
    email = models.EmailField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)