from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Poleras(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    talla = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()

class Usuarios(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = make_password(self.password)
        super(Usuarios, self).save(*args, **kwargs)