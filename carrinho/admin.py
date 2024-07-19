from django.contrib.admin import AdminSite
from .models import Carrinho, ItemCarrinho, Compra, ItemCompra
from django.contrib import admin
from produtos.admin import custom_admin_site

class CustomAdminSite(AdminSite):
    site_header = "ACG"
    site_title = "Administração ACG"
    index_title = "Bem-vindo à Administração"

custom_admin_site = CustomAdminSite(name='custom_admin')

class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'finalizado', 'criado_em', 'modificado', 'ativo')

class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrinho', 'produto', 'quantidade')

class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_compra', 'peso_total')

class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'compra', 'produto', 'quantidade')

admin.site.register(Carrinho, CarrinhoAdmin)
custom_admin_site.register(Carrinho, CarrinhoAdmin)
admin.site.register(ItemCarrinho, ItemCarrinhoAdmin)
custom_admin_site.register(ItemCarrinho, ItemCarrinhoAdmin)
admin.site.register(Compra, CompraAdmin)
custom_admin_site.register(Compra, CompraAdmin)
admin.site.register(ItemCompra, ItemCompraAdmin)
custom_admin_site.register(ItemCompra, ItemCompraAdmin)
