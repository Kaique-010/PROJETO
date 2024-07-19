# carrinho/urls.py

from django.urls import path
from .views import adicionar_ao_carrinho, carrinho_detalhe, checkout, completar_compra,limpar_carrinho, historico_compras
from carrinho import views

app_name = 'carrinho'

urlpatterns = [
    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar'),
    path('', carrinho_detalhe, name='carrinho_detalhe'),
    path('checkout/', checkout, name='checkout'),
    path('completar_compra/', completar_compra, name='completar_compra'),
    path('limpar/', limpar_carrinho, name='limpar'),
    path('historico/', historico_compras, name='historico_compras'),

]