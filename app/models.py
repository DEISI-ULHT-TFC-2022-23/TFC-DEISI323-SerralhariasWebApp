from django.contrib.auth.models import User
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
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    vat_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    billing_address = models.CharField(max_length=250, null=True, blank=True)

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    NEW = "New"
    PENDING_PAYMENT = "Pending Payment"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"
    ON_HOLD = "On Hold"

    STATE_CHOICES = [
        (NEW, NEW),
        (PENDING_PAYMENT, PENDING_PAYMENT),
        (PROCESSING, PROCESSING),
        (SHIPPED, SHIPPED),
        (DELIVERED, DELIVERED),
        (CANCELED, CANCELED),
        (ON_HOLD, ON_HOLD),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=4000, null=True, blank=True)
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=NEW,
    )