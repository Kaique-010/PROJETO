from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Login  
from representantes.models import Representante

# Formulário de Registro
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cnpj = forms.CharField(max_length=18, required=True)  
    representante = forms.ModelChoiceField(queryset=Representante.objects.all(),required=False,empty_label="Selecione um representante")
    cep = forms.CharField(max_length=10, required=False)  

    class Meta:
        model = Login
        fields = ('email', 'cnpj', 'password1', 'password2', 'representante', 'cep')

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        
        return cnpj

# Formulário de Login
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Alteramos o label para Email
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
