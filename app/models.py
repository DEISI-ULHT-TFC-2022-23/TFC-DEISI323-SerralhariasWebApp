from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories", null=True, blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return self.image.url

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    price = models.FloatField(null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('regular', 'Regular User'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    vat_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

