from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required


class IndexView(TemplateView):
    template_name = 'index.html'

class ContatoView(TemplateView):
    template_name = 'contato.html'

class RegistrarView(FormView):
    template_name = 'registrar.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('produtos_list')

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super().form_valid(form)
    
