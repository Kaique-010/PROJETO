from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Login  # Importe seu modelo de usuário personalizado

# Formulário de Registro
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cnpj = forms.CharField(max_length=14, required=True)

    class Meta:
        model = Login  # Usamos o modelo de usuário personalizado
        fields = ('email', 'cnpj', 'password1', 'password2')

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        # Aqui você pode adicionar validação adicional para o CNPJ, se necessário
        return cnpj

# Formulário de Login
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Alteramos o label para Email
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
