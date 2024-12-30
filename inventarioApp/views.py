from django.shortcuts import render, redirect
from .forms import LoginForm, productosForm
from .models import Usuarios  
from django.contrib.auth.hashers import check_password 
from django.contrib import messages
from .models import Productos, Movimiento
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json


#login de inicio de sesion
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Intenta obtener al usuario por el correo electrónico
                user = Usuarios.objects.get(email=email)

                # Verifica si la contraseña proporcionada es correcta
                if check_password(password, user.password):
                    #redirigimos al usuario dependiendo de su rol
                    if user.rol == 'Jefa':
                        return redirect('inicio')
                    elif user.rol == 'empleado':
                        return redirect('inicioEmp')
                    # Si la autenticación es correcta, redirige a la página de inventario
                    else:
                        return redirect('inicio')
                else:
                    # Si la contraseña es incorrecta, muestra un mensaje de error
                    messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')

            except Usuarios.DoesNotExist:
                # Si el usuario no existe, muestra un mensaje de error
                messages.error(request, 'Correo electrónico no registrado.')

        # Si el formulario no es válido, muestra los errores
        return render(request, 'inventarioApp/login.html', {'form': form})

    else:
        form = LoginForm()

    # Renderiza el formulario vacío en la solicitud GET
    return render(request, 'inventarioApp/login.html', {'form': form})


def inventario_view(request):
    return render(request, 'inventarioApp/inicio.html')

def inventario_viewEmp(request):
    return render(request, 'inventarioApp/inicioEmp.html')

def reports(request):
    return render(request, 'inventarioApp/reports.html')

# Inventario vista de administradores
def inventario(request):
    # Obtener la categoría seleccionada desde la URL
    categoria_seleccionada = request.GET.get('categoria')

    # Filtrar productos (puedes agregar lógica real si es necesario)
    productos = Productos.objects.all()

    # Actualización de stock
    if request.method == 'POST':
        producto_id = int(request.POST.get('producto_id'))
        nuevo_stock = int(request.POST.get('nuevo_stock'))

        producto = Productos.objects.get(id=producto_id)
        producto.stock = nuevo_stock
        producto.save()

        # Registrar el movimiento
        Movimiento.objects.create(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            categoria=producto.categoria,
            talla=producto.talla,
            precio=producto.precio,
            stock=nuevo_stock,
            accion="Ajuste de Stock (Jefe)"
        )

        return redirect('inventario')

    # Datos que pasamos al template
    data = {
        'seccion': 'inventario',
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,
    }

    return render(request, 'inventarioApp/inventario.html', data)

# Inventario vista de empleados
def inventarioEmp(request):
    # Obtener la categoría seleccionada desde la URL (GET request)
    categoria_seleccionada = request.GET.get('categoria')

    # Filtrar productos por categoría
    productos = []
    if categoria_seleccionada == 'Pantalones':
        productos = Productos.objects.all()
    elif categoria_seleccionada == 'Poleras':
        productos = Productos.objects.all()
    elif categoria_seleccionada == 'Zapatos':
        productos = Productos.objects.all()
    else:
        productos = list(Productos.objects.all())

    # Si se ha enviado un cambio de stock
    if request.method == 'POST':
        # Obtener el ID del producto y el nuevo stock desde el formulario
        producto_id = int(request.POST.get('producto_id'))
        nuevo_stock = int(request.POST.get('nuevo_stock'))

        # Obtener el producto y actualizar el stock
        producto = Productos.objects.get(id=producto_id)
        producto.stock = nuevo_stock
        producto.save()

        # Registrar el movimiento de "actualización de stock" en la tabla Movimiento
        Movimiento.objects.create(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            categoria=producto.categoria,
            talla=producto.talla,
            precio=producto.precio,
            stock=nuevo_stock,
            accion="Ajuste Stock (Empleado)"  # Tipo de acción	
        )

        # Redireccionar para evitar que se vuelva a enviar el formulario al refrescar la página
        return redirect('inventarioApp/inventarioEmp.html')

    # Datos que pasamos al template
    data = {
        'seccion': 'inventario',
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,
    }

    return render(request, 'inventarioApp/inventarioEmp.html', data)


def usuario(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'inventarioApp/usuarios.html', {'Usuarios': usuarios})

#agregar producto
def agregarProducto(request):
    form = productosForm()
    if request.method == 'POST':
        form = productosForm(request.POST)
        if form.is_valid():
            # Crear el nuevo producto
            nuevo_producto = Productos.objects.create(
                nombre=form.cleaned_data['nombre'],
                descripcion=form.cleaned_data['descripcion'],
                talla=form.cleaned_data['talla'],
                categoria=form.cleaned_data['categoria'],
                precio=form.cleaned_data['precio'],
                stock=form.cleaned_data['stock']
            )

            # Registrar el movimiento de "agregar" en la tabla Movimiento
            Movimiento.objects.create(
                nombre=nuevo_producto.nombre,
                categoria=nuevo_producto.categoria,
                talla=nuevo_producto.talla,
                precio=nuevo_producto.precio,
                stock=nuevo_producto.stock,
                accion="Agregar (Jefe)"  # Tipo de acción
            )

            return HttpResponseRedirect(reverse('inventario'))
    data = {'form': form}
    return render(request, 'inventarioApp/agregarProducto.html', data)

# Reportes de inventario
def reports(request):
    movimientos = Movimiento.objects.all()
    
    # Obtener filtros desde los parámetros GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    action_type = request.GET.get('action_type')

    # Filtrar movimientos en base a los filtros proporcionados
    if start_date:
        movimientos = movimientos.filter(fecha__gte=datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        movimientos = movimientos.filter(fecha__lte=datetime.strptime(end_date, '%Y-%m-%d'))
    if action_type:
        movimientos = movimientos.filter(accion=action_type)

    return render(request, 'inventarioApp/reports.html', {'movimientos': movimientos})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Productos, Movimiento

def ajustarStock(request, producto_id):
    if request.method == "POST":
        try:
            # Leer y validar datos
            data = json.loads(request.body)
            adjustment = int(data.get("adjustment", 0))
            
            if adjustment == 0:
                return JsonResponse({"status": "error", "message": "El ajuste no puede ser cero."}, status=400)

            producto = get_object_or_404(Productos, id=producto_id)
            new_stock = producto.stock + adjustment

            if new_stock < 0:
                return JsonResponse({"status": "error", "message": "El stock no puede ser negativo."}, status=400)

            # Actualizar el stock
            producto.stock = new_stock
            producto.save()

            # Registrar el movimiento
            Movimiento.objects.create(
                nombre=producto.nombre,
                categoria=producto.categoria,
                talla=producto.talla,
                precio=producto.precio,
                stock=producto.stock,
                accion="Ajuste"
            )

            return JsonResponse({"status": "success", "stock": producto.stock})

        except ValueError:
            return JsonResponse({"status": "error", "message": "Datos inválidos."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)


# Modificar un producto
def modificarProducto(request, producto_id):
    if request.method == 'POST':
        try:
            # Obtener el producto por ID usando el modelo correcto
            producto = get_object_or_404(Productos, id=producto_id)

            # Capturar los datos enviados en la solicitud
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoria = request.POST.get('categoria')
            talla = request.POST.get('talla')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            
            # Validar que los datos no están vacíos
            producto.nombre = nombre or producto.nombre
            producto.descripcion = descripcion or producto.descripcion
            producto.categoria = categoria or producto.categoria
            producto.talla = talla or producto.talla
            producto.precio = float(precio) if precio else producto.precio
            producto.stock = int(stock) if stock else producto.stock

            # Guardar cambios en la base de datos
            producto.save()

            # Registrar el movimiento de "modificación" en la tabla Movimiento
            Movimiento.objects.create(
                nombre=producto.nombre,
                categoria=producto.categoria,
                talla=producto.talla,
                precio=producto.precio,
                stock=producto.stock,
                accion="Modificación (Jefe)"  # Tipo de acción
            )

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


def eliminarProducto(request, producto_id):
    producto = Productos.objects.get(id=producto_id)
    producto.delete()

    # Registrar el movimiento de "eliminación" en la tabla Movimiento
    Movimiento.objects.create(
        nombre=producto.nombre,
        talla=producto.talla,
        categoria=producto.categoria,
        precio=producto.precio,
        stock=producto.stock,
        accion="Eliminación (Jefe)"  # Tipo de acción
    )
    return HttpResponseRedirect(reverse('inventario'))
    