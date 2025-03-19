from django.db import models

# Create your models here.
# models.py
from django.db import models

from django.db import models

class FashionItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='fashion_images/', blank=True, null=True)
    age_range = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=5, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    body_type = models.CharField(max_length=50, blank=True)
    occasion = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
