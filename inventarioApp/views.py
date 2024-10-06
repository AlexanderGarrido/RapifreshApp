from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Usuarios  
from django.contrib.auth.hashers import check_password 
from django.contrib import messages

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
                    if user.rol == 'jefa':
                        return redirect('inventario')
                    elif user.rol == 'empleado':
                        return redirect('invProduct')
                    # Si la autenticación es correcta, redirige a la página de inventario
                    return redirect('inventario')
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
    return render(request, 'inventarioApp/inventario.html')

def reports(request):
    return render(request, 'inventarioApp/reports.html')

def invProduct(request):
    # Obtener la categoría seleccionada desde la URL (GET request)
    categoria_seleccionada = request.GET.get('categoria')

    # Simulación de productos (esto debería ser reemplazado con tu modelo si es que tienes uno)
    productos = [
        {
            'id': 1,
            'nombre': 'Pantalones de cuero',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Pantalones',
            'precio': 1000,
            'stock': 6,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 2,
            'nombre': 'Pantalones de algodón',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Pantalones',
            'precio': 500,
            'stock': 0,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 3,
            'nombre': 'Pantalones de lona',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Pantalones',
            'precio': 800,
            'stock': 12,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 4,
            'nombre': 'Camiseta de algodón',
            'color':  'Blanco',
            'talla': 'M',
            'categoria': 'Camisetas',
            'precio': 200,
            'stock': 15,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 5,
            'nombre': 'Camiseta de lona',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Camisetas',
            'precio': 300,
            'stock': 2,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 6,
            'nombre': 'Camiseta de cuero',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Camisetas',
            'precio': 400,
            'stock': 18,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 7,
            'nombre': 'Zapatos de cuero',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Zapatos',
            'precio': 500,
            'stock': 10,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 8,
            'nombre': 'Zapatos de lona',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Zapatos',
            'precio': 600,
            'stock': 12,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
        {
            'id': 9,
            'nombre': 'Zapatos de algodón',
            'color':  'Negro',
            'talla': 'M',
            'categoria': 'Zapatos',
            'precio': 700,
            'stock': 5,
            'imagen': 'https://via.placeholder.com/150/#808080',
        },
    ]

    # Si se ha enviado un cambio de stock
    if request.method == 'POST':
        # Obtener el ID del producto y el nuevo stock desde el formulario
        producto_id = int(request.POST.get('producto_id'))
        nuevo_stock = int(request.POST.get('nuevo_stock'))

        # Actualizar el stock del producto en la lista (debería ser una actualización en la base de datos en un caso real)
        for producto in productos:
            if producto['id'] == producto_id:
                producto['stock'] = nuevo_stock
                break

        # Redireccionar para evitar que se vuelva a enviar el formulario al refrescar la página
        return redirect('invProduct')

    # Filtrar productos por categoría si se selecciona una categoría
    if categoria_seleccionada:
        productos = [producto for producto in productos if producto['categoria'] == categoria_seleccionada]

    # Datos que pasamos al template
    data = {
        'seccion': 'invProduct',
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,  # Para marcar la categoría seleccionada en el filtro
    }

    return render(request, 'inventarioApp/productos.html', data)