# models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField()

    proveedor = models.CharField(max_length=100)

    CATEGORIA_CHOICES = (
        ('Indumentaria', 'Indumentaria'),
        ('Herramientas', 'Herramientas'),
        ('Cajas', 'Cajas'),
        ('Film', 'Film'),
        ('Bolsa', 'Bolsa'),
    )
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='Indumentaria')

    def __str__(self):
        return f"{self.nombre} - {self.categoria} - Stock: {self.stock}"

# Manager personalizado para el modelo de usuario
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Usa set_password para hashear
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Los superusuarios deben estar activos
        extra_fields.setdefault('rol', 'Administrador') # Un superusuario suele ser el 'Administrador'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class Usuarios(AbstractBaseUser, PermissionsMixin): # Heredar de AbstractBaseUser y PermissionsMixin
    email = models.EmailField(max_length=100, unique=True)
    # password = models.CharField(max_length=128) # El campo password ya está en AbstractBaseUser
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    
    # Asegúrate de que los valores aquí coincidan con los que usas en los decoradores de views.py
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='Empleado')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Para acceso al admin de Django
    is_superuser = models.BooleanField(default=False) # Para superusuario de Django

    objects = CustomUserManager() # Asignar el manager personalizado

    USERNAME_FIELD = 'email' # Campo que se usará para el login
    REQUIRED_FIELDS = ['nombre', 'apellido', 'rol'] # Campos que se pedirán al crear un superusuario

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"

    # Métodos para compatibilidad con el sistema de autenticación de Django
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    def get_short_name(self):
        return self.nombre
        
class Movimiento(models.Model):
    # Relación con el producto (si no se elimina)
    producto_id = models.IntegerField(null=True, blank=True)  # ID del producto (referencia manual)
    nombre_producto = models.CharField(max_length=100, null=True, blank=True)  # Nombre del producto en ese momento
    proveedor = models.CharField(max_length=100, null=True, blank=True)  # Proveedor en ese momento
    categoria = models.CharField(max_length=50, null=True, blank=True)  # Categoría en ese momento

    # Estado del stock antes y después del movimiento
    stock_anterior = models.IntegerField(null=True, blank=True)
    stock_nuevo = models.IntegerField(null=True, blank=True)
    cantidad_ajustada = models.IntegerField(null=True, blank=True)  # Cambio neto en el stock

    # Información sobre el tipo de acción
    accion = models.CharField(max_length=50)  # Ej: "Agregar", "Editar", "Eliminar", etc.
    fecha = models.DateTimeField(auto_now_add=True)

    # Usuario responsable del cambio
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    usuario_nombre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        usuario_info = f" por {self.usuario_nombre}" if self.usuario_nombre else ""
        return f"{self.accion} - {self.nombre_producto or 'N/A'}{usuario_info} - {self.fecha.strftime('%d-%m-%Y %H:%M')}"

    class Meta:
        ordering = ['-fecha']

