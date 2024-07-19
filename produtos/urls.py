from django.urls import path
from .views import ProdutosListView, ProdutosCreateView, ProdutosUpdateView, ProdutoDetailView, GrupoDetailView, GrupoProdutosView, filtrar_produtos
from produtos import views

urlpatterns = [
    path('', ProdutosListView.as_view(), name='produtos_list'),  # URL para listar produtos
    path('produto/novo/', ProdutosCreateView.as_view(), name='produtos_create'),  # URL para criar um novo produto
    path('produto/<int:pk>/editar/', ProdutosUpdateView.as_view(), name='produtos_update'),  # URL para editar um produto
    path('produto/<int:pk>/', ProdutoDetailView.as_view(), name='produto_detalhe'),  # URL para detalhes de um produto
    path('grupo/<int:pk>/', GrupoDetailView.as_view(), name='grupo_detalhe'),  # URL para detalhes de um grupo
    path('grupo/<int:pk>/produtos/', GrupoProdutosView.as_view(), name='grupo_produtos'),
    path('filtrar_produtos/', filtrar_produtos, name='filtrar_produtos'),


]
