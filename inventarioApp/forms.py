# forms.py
from django import forms
from .models import Productos, Usuarios # Importar Usuarios también
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm # Importar el UserCreationForm base de Django

# Importar las opciones directamente del modelo Productos
# No es necesario si usas ModelForm y los campos son ChoiceField en el modelo
# talla_choices = Productos.talla_choices
# categoria_choices = Productos.categoria_choices


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}),
        error_messages={
            'required': 'El campo de correo electrónico es obligatorio.',
            'invalid': 'Introduce un correo electrónico válido.'
        }
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}),
        min_length=4,
        max_length=6,
        error_messages={
            'required': 'El campo de contraseña es obligatorio.',
            'min_length': 'La contraseña debe tener al menos 4 caracteres.',
            'max_length': 'La contraseña no debe tener más de 6 caracteres.'
        }
    )

# Usar ModelForm para simplificar la creación del formulario de productos
class ProductosForm(forms.ModelForm): # Renombrado a ProductosForm (capitalizado)
    class Meta:
        model = Productos
        fields = ['nombre', 'descripcion', 'categoria', 'talla', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock del producto'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),     # Django usa Select para ChoiceField  
            'categoria': forms.Select(attrs={'class': 'form-control'}), # Django usa Select para ChoiceField
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto', 'rows': 3}),
        }
    
    # Si quisieras añadir validaciones adicionales o modificar campos, lo harías aquí
    # Por ejemplo, para precio, si quieres un DecimalField en lugar de NumberInput:
    # precio = forms.DecimalField(max_digits=10, decimal_places=2, 
    #                             widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio del producto'}))


# Formulario para la creación de usuarios por el administrador
class UsuarioCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        min_length=4,
        max_length=6,
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 4 caracteres.',
            'max_length': 'La contraseña no debe tener más de 6 caracteres.'
        }
    )
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma la contraseña'}),
        min_length=4,
        max_length=6,
        error_messages={
            'required': 'La confirmación de contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 4 caracteres.',
            'max_length': 'La contraseña no debe tener más de 6 caracteres.'
        }
    )

    class Meta:
        model = Usuarios
        # Se han eliminado 'is_active' y 'is_staff' de los campos del formulario.
        # Ahora se gestionarán directamente en el método save() para asegurar su valor.
        fields = ['email', 'nombre', 'apellido', 'rol']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        # Aseguramos que el usuario esté activo al ser creado
        user.is_active = True 
        
        # Configuramos is_staff basado en el rol seleccionado
        if user.rol == 'Administrador':
            user.is_staff = True
        else: # Para el rol 'Empleado'
            user.is_staff = False 

        if commit:
            user.save()
        return user

