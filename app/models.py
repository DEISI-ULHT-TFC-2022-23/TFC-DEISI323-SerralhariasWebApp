from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    pass

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class addProduct(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    


