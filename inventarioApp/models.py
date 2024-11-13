from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
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
    
    ROL_CHOICES = [
        ('jefa', 'Jefa'),
        ('empleado', 'Empleado'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='empleado')

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = make_password(self.password)
        super(Usuarios, self).save(*args, **kwargs)
        
class Movimiento(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    talla = models.CharField(max_length=10)
    categoria = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    accion = models.CharField(max_length=20)  # Ej. "agregar", "editar", "eliminar"
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.nombre} - {self.fecha}"