from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class CustomUserCreationForm(forms.Form):
    """
    Formulario personalizado que permite espacios en el nombre de usuario
    """
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        help_text='Puede contener letras, números y espacios.',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': 'Ingresa tu nombre completo'
        })
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': 'Crea una contraseña segura'
        })
    )
    
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500',
            'placeholder': 'Confirma tu contraseña'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Permitir espacios pero eliminar espacios al inicio y final
            username = username.strip()
            if not username:
                raise forms.ValidationError('El nombre de usuario no puede estar vacío.')
            
            # Verificar que no exista ya
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Este nombre de usuario ya está en uso.')
                
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        return user
