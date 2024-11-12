from django.shortcuts import render, redirect
from .forms import LoginForm 
from .models import Usuarios  
from django.contrib.auth.hashers import check_password 
from django.contrib import messages
from .models import Poleras, Pantalones, Zapatos
from django.urls import reverse
from django.http import HttpResponseRedirect

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

def inventario(request):
    # Obtener la categoría seleccionada desde la URL (GET request)
    categoria_seleccionada = request.GET.get('categoria')

    # Dependiendo de la categoría seleccionada, obtenemos los productos correspondientes
    productos = []
    if categoria_seleccionada == 'Pantalones':
        productos = Pantalones.objects.all()
    elif categoria_seleccionada == 'Camisetas':
        productos = Poleras.objects.all()  # Asumimos que "Camisetas" corresponde a "Poleras"
    elif categoria_seleccionada == 'Zapatos':
        productos = Zapatos.objects.all()
    else:
        # Si no hay categoría seleccionada, obtenemos todos los productos de todas las categorías
        productos = list(Poleras.objects.all()) + list(Pantalones.objects.all()) + list(Zapatos.objects.all())

    # Si se ha enviado un cambio de stock
    if request.method == 'POST':
        # Obtener el ID del producto y el nuevo stock desde el formulario
        producto_id = int(request.POST.get('producto_id'))
        nuevo_stock = int(request.POST.get('nuevo_stock'))

        # Dependiendo de la categoría del producto, actualizamos el stock
        if categoria_seleccionada == 'Pantalones':
            producto = Pantalones.objects.get(id=producto_id)
        elif categoria_seleccionada == 'Camisetas':
            producto = Poleras.objects.get(id=producto_id)
        elif categoria_seleccionada == 'Zapatos':
            producto = Zapatos.objects.get(id=producto_id)
        
        # Actualizar el stock en la base de datos
        producto.stock = nuevo_stock
        producto.save()

        # Redireccionar para evitar que se vuelva a enviar el formulario al refrescar la página
        return redirect('inventario')

    # Datos que pasamos al template
    data = {
        'seccion': 'inventario',
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,  # Para marcar la categoría seleccionada en el filtro
    }

    return render(request, 'inventarioApp/inventario.html', data)

def inventarioEmp(request):
    # Obtener la categoría seleccionada desde la URL (GET request)
    categoria_seleccionada = request.GET.get('categoria')

    # Dependiendo de la categoría seleccionada, obtenemos los productos correspondientes
    productos = []
    if categoria_seleccionada == 'Pantalones':
        productos = Pantalones.objects.all()
    elif categoria_seleccionada == 'Camisetas':
        productos = Poleras.objects.all()  # Asumimos que "Camisetas" corresponde a "Poleras"
    elif categoria_seleccionada == 'Zapatos':
        productos = Zapatos.objects.all()
    else:
        # Si no hay categoría seleccionada, obtenemos todos los productos de todas las categorías
        productos = list(Poleras.objects.all()) + list(Pantalones.objects.all()) + list(Zapatos.objects.all())

    # Si se ha enviado un cambio de stock
    if request.method == 'POST':
        # Obtener el ID del producto y el nuevo stock desde el formulario
        producto_id = int(request.POST.get('producto_id'))
        nuevo_stock = int(request.POST.get('nuevo_stock'))

        # Dependiendo de la categoría del producto, actualizamos el stock
        if categoria_seleccionada == 'Pantalones':
            producto = Pantalones.objects.get(id=producto_id)
        elif categoria_seleccionada == 'Camisetas':
            producto = Poleras.objects.get(id=producto_id)
        elif categoria_seleccionada == 'Zapatos':
            producto = Zapatos.objects.get(id=producto_id)
        
        # Actualizar el stock en la base de datos
        producto.stock = nuevo_stock
        producto.save()

        # Redireccionar para evitar que se vuelva a enviar el formulario al refrescar la página
        return redirect('inventario')

    # Datos que pasamos al template
    data = {
        'seccion': 'inventario',
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,  # Para marcar la categoría seleccionada en el filtro
    }

    return render(request, 'inventarioApp/inventarioEmp.html', data)


def usuario(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'inventarioApp/usuarios.html', {'Usuarios': usuarios})
