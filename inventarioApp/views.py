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
                        return redirect('pantalones')
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

def pantalones(request):
    data = {
        'seccion': 'Pantalones',
        'productos': [ 
            {
                'id': 1,
                'nombre': 'Pantalones de cuero',
                'precio': 1000.0,
                'descripcion': 'Pantalones de cuero de alta calidad',
                'imagen': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQD0rjKrnkIKHwqtrncrSNSb9R6if2BdE-76A&s',
            },
            {
                'id': 2,
                'nombre': 'Pantalones de algodón',
                'precio': 500.0,
                'descripcion': 'Pantalones de algodón de alta calidad',
                'imagen': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQa7EVRWQiGGGFcGTDZsCVYN9VcQcF3gVcL4g&s',
            },
            {
                'id': 3,
                'nombre': 'Pantalones de lona',
                'precio': 800.0,
                'descripcion': 'Pantalones de lona de alta calidad',
                'imagen': 'https://treck.vtexassets.com/arquivos/ids/168163/06-01-363-T-2XL_06-01-363-F1_1665687004101-1300.jpg?v=638412803955530000',
            },
        ]
    }
    return render(request, 'inventarioApp/productos.html', data)

def camisetas(request):
    data = {
        'seccion': 'Camisetas',
        'productos': [
            {
                'id': 4,
                'nombre': 'Camiseta de algodón',
                'precio': 200.0,
                'descripcion': 'Camiseta de algodón de alta calidad',
                'imagen': 'https://via.placeholder.com/150/ff0000',
            },
            {
                'id': 5,
                'nombre': 'Camiseta de lona',
                'precio': 300.0,
                'descripcion': 'Camiseta de lona de alta calidad',
                'imagen': 'https://via.placeholder.com/150/ff0000',
            },
            {
                'id': 6,
                'nombre': 'Camiseta de cuero',
                'precio': 400.0,
                'descripcion': 'Camiseta de cuero de alta calidad',
                'imagen': 'https://via.placeholder.com/150/ff0000',
            },
        ]
    }
    return render(request, 'inventarioApp/productos.html', data)

def zapatos(request):
    data = {
        'seccion': 'Zapatos',
        'productos': [
            {
                'id': 7,
                'nombre': 'Zapatos de cuero',
                'precio': 500.0,
                'descripcion': 'Zapatos de cuero de alta calidad',
                'imagen': 'https://www.16hrs.cl/127946-home_default/zapato-vestir-16-hrs.jpg',
            },
            {
                'id': 8,
                'nombre': 'Zapatos de lona',
                'precio': 600.0,
                'descripcion': 'Zapatos de lona de alta calidad',
                'imagen': 'https://cdnx.jumpseller.com/www-san-antonio-cl/image/42256515/resize/1280/1280?1700252035',
            },
            {
                'id': 9,
                'nombre': 'Zapatos de algodón',
                'precio': 700.0,
                'descripcion': 'Zapatos de algodón de alta calidad',
                'imagen': 'https://segurycel.vteximg.com.br/arquivos/ids/157875-1000-1000/7243501020500038.jpg?v=636965692018000000',
            },
        ]
    }
    return render(request, 'inventarioApp/productos.html', data)