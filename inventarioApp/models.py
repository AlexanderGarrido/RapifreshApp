# models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Cambiado a DecimalField para precios
    categoria_choices = (
        ('Pantalones', 'Pantalones'),
        ('Poleras', 'Poleras'),
        ('Zapatos', 'Zapatos'),
    )
    categoria = models.CharField(max_length=100, choices=categoria_choices, default='Poleras')
    talla_choices = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    )
    talla = models.CharField(max_length=50, choices=talla_choices, default='S') # Añadido choices aquí
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

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
    # Campos para el producto involucrado en el movimiento
    # Usar ForeignKey si quieres integridad referencial y el producto NO se elimina
    # Si el producto puede ser eliminado y quieres mantener el registro del movimiento,
    # entonces IntegerField es adecuado, pero pierdes la integridad referencial.
    producto_id = models.IntegerField(null=True, blank=True) # ID del producto
    nombre_producto = models.CharField(max_length=100, null=True, blank=True) # Nombre del producto en el momento del movimiento
    descripcion = models.CharField(max_length=200, blank=True, null=True) # Descripción del producto
    categoria = models.CharField(max_length=50, null=True, blank=True) # Categoría del producto
    talla = models.CharField(max_length=10, null=True, blank=True) # Talla del producto
    color = models.CharField(max_length=50, blank=True, null=True) # Campo opcional, si es relevante

    # Campos para registrar el estado antes y después del movimiento
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_anterior = models.IntegerField(null=True, blank=True)
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_nuevo = models.IntegerField(null=True, blank=True)
    cantidad_ajustada = models.IntegerField(null=True, blank=True) # Cantidad específica ajustada (para incrementos/decrementos)

    # Información del movimiento
    accion = models.CharField(max_length=50)  # Ej. "Agregar (Administrador)", "Modificación (Administrador)", "Ajuste (Empleado)", "Eliminación (Administrador)"
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Añadido: Campo para registrar qué usuario hizo el movimiento
    # Si el usuario se elimina, el campo se pondrá a NULL
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    usuario_nombre = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        # Muestra el tipo de acción, el nombre del producto, quién lo hizo y la fecha
        usuario_info = f" por {self.usuario_nombre}" if self.usuario_nombre else ""
        return f"{self.accion} - {self.nombre_producto or 'N/A'}{usuario_info} - {self.fecha.strftime('%d-%m-%Y %H:%M')}"

    class Meta:
        # Ordenar los movimientos por fecha descendente por defecto
        ordering = ['-fecha']
