from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Aquí iría la lógica de autenticación

            # Si la autenticación es exitosa, redirige a la página de inventario
            return redirect('inventario')
        else:
            # Si el formulario no es válido, muestra los errores
            return render(request, 'inventarioApp/login.html', {'form': form})
    else:
        form = LoginForm()
    
    # Renderiza el formulario vacío en la solicitud GET
    return render(request, 'inventarioApp/login.html', {'form': form})

def inventario_view(request):
    return render(request, 'inventarioApp/inventario.html')
