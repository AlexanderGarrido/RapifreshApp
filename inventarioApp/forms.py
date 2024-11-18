from django import forms


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

class productosForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=200)
    color = forms.CharField(max_length=100)
    talla = forms.CharField(max_length=50)
    categoria = forms.CharField(max_length=100)
    precio = forms.IntegerField()    
    stock = forms.IntegerField()

    nombre.widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del producto'})
    descripcion.widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción del producto'})
    color.widget.attrs.update({'class': 'form-control', 'placeholder': 'Color del producto'})
    talla.widget.attrs.update({'class': 'form-control', 'placeholder': 'Talla del producto'})
    categoria.widget.attrs.update({'class': 'form-control', 'placeholder': 'Categoría del producto'})
    precio.widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio del producto'})
    stock.widget.attrs.update({'class': 'form-control', 'placeholder': 'Stock del producto'})
