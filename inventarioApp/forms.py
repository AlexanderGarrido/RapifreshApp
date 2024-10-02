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