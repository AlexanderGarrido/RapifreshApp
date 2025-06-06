# admin.py
from django.contrib import admin

# Register your models here.

from inventarioApp.models import *


class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria','proveedor', 'stock')
    # Añade filtros y búsqueda para facilitar la gestión
    list_filter = ('categoria', 'proveedor')
    search_fields = ('nombre', 'descripcion')

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellido', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('email', 'nombre', 'apellido')

class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('accion', 'nombre_producto', 'cantidad_ajustada', 'stock_anterior', 'stock_nuevo', 'fecha')
    list_filter = ('accion', 'fecha')
    search_fields = ('nombre_producto', 'accion')
    readonly_fields = ('fecha',) # La fecha se establece automáticamente

admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Productos, ProductosAdmin)
admin.site.register(Movimiento, MovimientoAdmin) # Registrar el modelo Movimiento

