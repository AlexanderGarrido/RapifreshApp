from django.db import models

# Create your models here.

class Poleras(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    talla = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()