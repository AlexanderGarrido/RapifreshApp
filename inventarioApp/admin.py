from django.contrib import admin

# Register your models here.

from inventarioApp.models import *

class PolerasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'talla', 'categoria', 'precio', 'stock')

class PantalonesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'talla', 'categoria', 'precio', 'stock')

class ZapatosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'talla', 'categoria', 'precio', 'stock')

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellido', 'rol')

admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Poleras, PolerasAdmin)
admin.site.register(Pantalones, PantalonesAdmin)
admin.site.register(Zapatos, ZapatosAdmin)