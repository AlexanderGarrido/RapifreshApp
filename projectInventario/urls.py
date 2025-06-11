"""
URL configuration for projectInventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventarioApp.views import *

# Importaciones para servir archivos estáticos en desarrollo
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'), # Nueva URL para cerrar sesión
    path('inicio/', inventario_view, name='inicio'),
    path('inventario/', inventario, name='inventario'),
    path('reports/', reports, name='reports'),
    path('inventarioEmp/', inventarioEmp, name='inventarioEmp'),
    path('inicioEmp/', inventario_viewEmp, name='inicioEmp'),
    path('usuarios/', usuario, name='usuarios'),
    path('usuarios/agregar/', agregarUsuario, name='agregarUsuario'), # Nueva URL para agregar usuarios
    path('agregarProducto/', agregarProducto, name='agregarProducto'),
    path('ajusteStock/<int:producto_id>/', ajustarStock, name='ajustarStock'),
    path('modificarProducto/<int:producto_id>/', modificarProducto, name='modificarProducto'),
    path('eliminarProducto/<int:producto_id>/', eliminarProducto, name='eliminarProducto'),
    path('qr-scan/', qr_scan_page, name='qr_scan_page'),
    path('process-qr/', process_qr_code, name='process_qr_code'),
    path('generate-qr/', generate_qr_code, name='generate_qr_code'),
    path('create-qr/', create_qr_code, name='create_qr_code'),
    path('galpon/', galpon_view, name='galpon'),

]

# Servir archivos estáticos solo en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

