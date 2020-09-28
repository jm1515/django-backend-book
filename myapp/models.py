from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    author = models.CharField(max_length=256, null=True, blank=True)
    year = models.PositiveIntegerField(default=0, null=True, blank=True)
    price= models.FloatField(default=-1.0, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    bestseller= models.BooleanField(default=False)