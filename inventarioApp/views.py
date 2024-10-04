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
