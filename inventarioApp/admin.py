from django.contrib import admin

# Register your models here.

from inventarioApp.models import *


class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'color', 'precio', 'stock', 'categoria', 'talla')

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellido', 'rol')

admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Productos, ProductosAdmin)