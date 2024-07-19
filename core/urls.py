from django.urls import path
from .views import IndexView, ContatoView, LoginView, RegistrarView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('index/',IndexView.as_view(), name='Index'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('login/', LoginView.as_view(), name='login'),
    path('registrar/', RegistrarView.as_view(), name= 'registrar'),
   
]
