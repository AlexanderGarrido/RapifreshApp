# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ProductosForm, UsuarioCreationForm # Importar ProductosForm y el nuevo UsuarioCreationForm
from .models import Usuarios, Productos, Movimiento
# Importaciones para autenticación de Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.db.models import Q
import json
#Nuevos imports
import qrcode
import io
import base64
from django.views.decorators.http import require_http_methods

# --- Decoradores personalizados para roles ---

def is_Administrador(user):
    """Verifica si el usuario es 'Administrador'."""
    # Asegúrate de que 'Administrador' coincida con el valor en ROL_CHOICES de models.py
    return user.is_authenticated and user.rol == 'Administrador'

def is_empleado(user):
    """Verifica si el usuario es 'Empleado'."""
    # Asegúrate de que 'Empleado' coincida con el valor en ROL_CHOICES de models.py
    return user.is_authenticated and user.rol == 'Empleado'

def Administrador_required(view_func):
    """Decorador que requiere que el usuario sea 'Administrador'."""
    decorated_view_func = login_required(user_passes_test(is_Administrador, login_url='login', redirect_field_name=None)(view_func))
    return decorated_view_func

def Empleado_required(view_func):
    """Decorador que requiere que el usuario sea 'Empleado'."""
    decorated_view_func = login_required(user_passes_test(is_empleado, login_url='login', redirect_field_name=None)(view_func))
    return decorated_view_func

# --- Vistas ---


#Vista del QR
def qr_scan_page(request):
    """Vista que muestra la página del escáner QR"""
    return render(request, 'inventarioApp/qr_scanner.html')

@csrf_exempt
def process_qr_code(request):
    """Vista que procesa el código QR escaneado"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_code = data.get('qr_code', '')
            
            # Aquí puedes procesar el código QR como necesites
            # Por ejemplo, buscar en la base de datos, validar, etc.
            
            # Ejemplo de procesamiento básico:
            if qr_code:
                # Procesa tu código QR aquí
                result = {
                    'success': True,
                    'message': f'Código QR procesado: {qr_code}',
                    'qr_data': qr_code
                }
                
                # Opcional: Guardar en base de datos o hacer alguna acción
                # process_qr_data(qr_code)
                
            else:
                result = {
                    'success': False,
                    'message': 'No se recibió código QR válido'
                }
                
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error al procesar los datos'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })#


#Generador de QR
def generate_qr_code(request):
    """Vista para mostrar el formulario de generación de códigos QR"""
    return render(request, 'inventarioApp/qr_generator.html')

@csrf_exempt
@require_http_methods(["POST"])
def create_qr_code(request):
    """Vista AJAX para crear el código QR"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({
                'success': False,
                'message': 'Por favor ingresa el texto o URL para generar el código QR'
            })
        
        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Crear la imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return JsonResponse({
            'success': True,
            'message': 'Código QR generado exitosamente',
            'qr_image': f'data:image/png;base64,{img_str}',
            'text': text
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Error en los datos enviados'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al generar el código QR: {str(e)}'
        })


# Login de inicio de sesion
def login_view(request):
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirigir según su rol
        if request.user.rol == 'Administrador':
            return redirect('inicio')
        elif request.user.rol == 'Empleado': # Cambiado a 'Empleado'
            return redirect('inicioEmp')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Autenticar al usuario usando el backend de autenticación de Django
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Iniciar sesión al usuario
                login(request, user)
                messages.success(request, f'Bienvenido, {user.nombre}!')
                # Redirigir según el rol del usuario
                if user.rol == 'Administrador':
                    return redirect('inicio')
                elif user.rol == 'Empleado': # Cambiado a 'Empleado'
                    return redirect('inicioEmp')
                else:
                    # Rol desconocido, redirigir a una página por defecto o mostrar error
                    messages.error(request, 'Rol de usuario no reconocido.')
                    return redirect('login')
            else:
                # Si la autenticación falla, muestra un mensaje de error
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
        else:
            # Si el formulario no es válido, los errores se mostrarán en la plantilla
            pass # Los errores del formulario se manejan en la plantilla

    else: # GET request
        form = LoginForm()

    return render(request, 'inventarioApp/login.html', {'form': form})

# Logout de sesion
@login_required # Asegura que solo usuarios logueados puedan cerrar sesión
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


@Administrador_required # Solo accesible por 'Administrador'
def inventario_view(request):
    """Vista para el panel de inicio del rol 'Administrador'."""
    return render(request, 'inventarioApp/inicio.html')

@Empleado_required # Solo accesible por 'Empleado'
def inventario_viewEmp(request):
    """Vista para el panel de inicio del rol 'Empleado'."""
    return render(request, 'inventarioApp/inicioEmp.html')

@Administrador_required # Solo accesible por 'Administrador'
def inventario(request):
    """
    Vista para la gestión de inventario por parte de administradores (Administrador).
    Permite ver, agregar, modificar y eliminar productos, con opciones de filtro.
    """
    productos = Productos.objects.all() # Obtener todos los productos

    # Obtener parámetros de filtro de la URL
    nombre_filter = request.GET.get('nombre')
    categoria_filter = request.GET.get('categoria')
    proveedor_filter = request.GET.get('proveedor')
    stock_min_filter = request.GET.get('stock_min')

    # Aplicar filtros si están presentes
    if nombre_filter:
        productos = productos.filter(nombre__icontains=nombre_filter)
    if categoria_filter:
        productos = productos.filter(categoria__icontains=categoria_filter)
    if proveedor_filter:
        productos = productos.filter(proveedor__icontains=proveedor_filter)
    if stock_min_filter:
        try:
            stock_min_filter = int(stock_min_filter)
            productos = productos.filter(stock__gte=stock_min_filter)
        except ValueError:
            # Puedes añadir un mensaje de error si el stock_min no es un número válido
            messages.error(request, 'El valor de "Stock Mínimo" debe ser un número entero.')
            pass # Continúa sin aplicar este filtro si hay un error de valor

    # Datos que pasamos al template
    data = {
        'seccion': 'inventario',
        'productos': productos,
        'request_get': request.GET # Pasa request.GET para mantener los valores de los filtros en la plantilla
    }
    return render(request, 'inventarioApp/inventario.html', data)

@Empleado_required # Solo accesible por 'Empleado'
def inventarioEmp(request):
    """
    Vista para la gestión de inventario por parte de empleados.
    Permite ver y ajustar el stock de productos.
    """
    productos = Productos.objects.all() # Los empleados ven todos los productos

    # Datos que pasamos al template
    data = {
        'seccion': 'inventario',
        'productos': productos,
    }
    return render(request, 'inventarioApp/inventarioEmp.html', data)

@Administrador_required # Solo accesible por 'Administrador'
def usuario(request):
    """Vista para la gestión de usuarios."""
    usuarios = Usuarios.objects.all()
    return render(request, 'inventarioApp/usuarios.html', {'Usuarios': usuarios})

@Administrador_required # Solo accesible por 'Administrador'
def agregarUsuario(request):
    """
    Vista para agregar un nuevo usuario (Administrador o Empleado).
    Solo accesible por 'Administrador'.
    """
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.email} creado exitosamente como {user.rol}.')
            return redirect('usuarios') # Redirigir a la lista de usuarios
        else:
            messages.error(request, 'Hubo un error al crear el usuario. Por favor, revisa los campos.')
    else:
        form = UsuarioCreationForm()
    return render(request, 'inventarioApp/agregarUsuario.html', {'form': form})


@Administrador_required
def agregarProducto(request):
    """
    Vista para agregar un nuevo producto al inventario.
    Registra el movimiento en la tabla Movimiento.
    """
    form = ProductosForm()
    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            nuevo_producto = form.save()

            # Registrar el movimiento de "agregar" en la tabla Movimiento
            Movimiento.objects.create(
                producto_id=nuevo_producto.id,
                nombre_producto=nuevo_producto.nombre,
                categoria=nuevo_producto.categoria,
                proveedor=nuevo_producto.proveedor,
                stock_anterior=0,  # ← AGREGADO: Para productos nuevos el stock anterior es 0
                stock_nuevo=nuevo_producto.stock,
                accion="Agregar (Administrador)",
                cantidad_ajustada=nuevo_producto.stock,
                usuario=request.user if request.user.is_authenticated else None,
                usuario_nombre=request.user.get_full_name() if request.user.is_authenticated else "Administrador",
            )

            messages.success(request, 'Producto agregado exitosamente.')
            return HttpResponseRedirect(reverse('inventario'))
        else:
            messages.error(request, 'Hubo un error al agregar el producto. Por favor, revisa los campos.')
    
    data = {'form': form}
    return render(request, 'inventarioApp/agregarProducto.html', data)

@Administrador_required # Solo accesible por 'Administrador'
def reports(request):
    """
    Vista para generar reportes de movimientos de inventario.
    Permite filtrar por rango de fechas y tipo de acción.
    """
    movimientos = Movimiento.objects.all()
    
    # Obtener filtros desde los parámetros GET
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    action_type = request.GET.get('action_type')

    # Filtrar movimientos en base a los filtros proporcionados
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            movimientos = movimientos.filter(fecha__gte=start_date)
        except ValueError:
            messages.error(request, 'Formato de fecha de inicio inválido.')
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # Para incluir el día completo, se ajusta a las 23:59:59
            movimientos = movimientos.filter(fecha__lte=end_date.replace(hour=23, minute=59, second=59))
        except ValueError:
            messages.error(request, 'Formato de fecha de fin inválido.')
    if action_type:
        movimientos = movimientos.filter(accion=action_type)

    return render(request, 'inventarioApp/reports.html', {'movimientos': movimientos})

@Empleado_required
def ajustarStock(request, producto_id):
    """
    Vista AJAX para ajustar el stock de un producto.
    Registra el movimiento en la tabla Movimiento.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            adjustment = int(data.get("adjustment", 0))
            
            if adjustment == 0:
                return JsonResponse({"status": "error", "message": "El ajuste no puede ser cero."}, status=400)

            producto = get_object_or_404(Productos, id=producto_id)
            stock_anterior = producto.stock  # Guardar el stock anterior
            new_stock = producto.stock + adjustment

            if new_stock < 0:
                return JsonResponse({"status": "error", "message": "El stock no puede ser negativo."}, status=400)

            # Actualizar el stock
            producto.stock = new_stock
            producto.save()

            accion_movimiento = "Ajuste (Empleado)"
            
            # Registrar el movimiento
            Movimiento.objects.create(
                producto_id=producto.id,
                nombre_producto=producto.nombre,
                categoria=producto.categoria,
                proveedor=producto.proveedor,
                stock_anterior=stock_anterior,  # ← CORREGIDO: Ahora sí se guarda el stock anterior
                stock_nuevo=producto.stock,
                accion=accion_movimiento,
                cantidad_ajustada=adjustment,
                usuario=request.user if request.user.is_authenticated else None,
                usuario_nombre=request.user.get_full_name() if request.user.is_authenticated else "Empleado",
            )

            return JsonResponse({"status": "success", "stock": producto.stock, "message": "Stock ajustado correctamente."})

        except ValueError:
            return JsonResponse({"status": "error", "message": "Datos de ajuste inválidos. Asegúrate de que el ajuste sea un número entero."}, status=400)
        except Exception as e:
            print(f"Error al ajustar el producto: {e}")
            return JsonResponse({"status": "error", "message": f"Error interno del servidor: {str(e)}"}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)


@Administrador_required
def modificarProducto(request, producto_id):
    """
    Vista AJAX para modificar los detalles de un producto.
    Registra el movimiento en la tabla Movimiento.
    """
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Productos, id=producto_id)

            # Guardar los valores anteriores para el registro de movimiento
            nombre_anterior = producto.nombre
            categoria_anterior = producto.categoria
            proveedor_anterior = producto.proveedor
            stock_anterior = producto.stock  # ← AGREGADO: Guardar stock anterior

            nombre = request.POST.get('nombre')
            categoria = request.POST.get('categoria')
            proveedor = request.POST.get('proveedor')
            stock_str = request.POST.get('stock')

            # Validar y convertir stock
            stock_nuevo = producto.stock
            if stock_str:
                try:
                    stock_nuevo = int(stock_str)
                except ValueError:
                    return JsonResponse({'success': False, 'error': 'Stock inválido. Debe ser un número entero.'}, status=400)

            # Actualizar los campos del producto
            producto.nombre = nombre if nombre else producto.nombre
            producto.categoria = categoria if categoria else producto.categoria
            producto.proveedor = proveedor if proveedor else producto.proveedor
            producto.stock = stock_nuevo

            producto.save()

            # Registrar el movimiento de "modificación"
            Movimiento.objects.create(
                producto_id=producto.id,
                nombre_producto=nombre_anterior,
                categoria=categoria_anterior,
                proveedor=proveedor_anterior,
                stock_anterior=stock_anterior,  # ← AGREGADO: Ahora se guarda el stock anterior
                stock_nuevo=producto.stock,
                accion="Modificación (Administrador)",
                usuario=request.user if request.user.is_authenticated else None,
                usuario_nombre=request.user.get_full_name() if request.user.is_authenticated else "Administrador",
            )

            return JsonResponse({'success': True, 'message': 'Producto modificado correctamente.'})
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return JsonResponse({'success': False, 'error': str(e), 'message': 'Error al actualizar el producto.'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)



@Administrador_required
def eliminarProducto(request, producto_id):
    """
    Vista para eliminar un producto del inventario.
    Registra el movimiento en la tabla Movimiento.
    """
    producto = get_object_or_404(Productos, id=producto_id)
    
    # Registrar el movimiento de "eliminación" antes de eliminar el producto
    Movimiento.objects.create(
        producto_id=producto.id,
        nombre_producto=producto.nombre,
        categoria=producto.categoria,
        proveedor=producto.proveedor,
        stock_anterior=producto.stock,  # ← AGREGADO: Guardar el stock que tenía antes de eliminar
        stock_nuevo=0,
        accion="Eliminación (Administrador)",
        cantidad_ajustada=-producto.stock,
        usuario=request.user if request.user.is_authenticated else None,
        usuario_nombre=request.user.get_full_name() if request.user.is_authenticated else "Administrador",
    )
    
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return HttpResponseRedirect(reverse('inventario'))


def galpon_view(request):
    return render(request, 'inventarioApp/galpon.html')

