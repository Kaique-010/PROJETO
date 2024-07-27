from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Produtos, Grupo, Familia, Colecao, Localidade
from carrinho.models import Carrinho, ItemCarrinho, Compra, ItemCompra
from representantes.models import Representante
from formasrecebimento.models import FormasRecebimento

class CustomAdminSite(AdminSite):
    site_header = "ACG"
    site_title = "Administração ACG"
    index_title = "Bem-vindo à Administração"

custom_admin_site = CustomAdminSite(name='custom_admin')

# Customizando a administração do modelo Produtos
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo', 'familia', 'colecao', 'ativo', 'imagem_tag', 'id')
    list_filter = ('grupo', 'familia', 'colecao', 'ativo')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('imagem_tag',)
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'grupo', 'familia', 'colecao', 'ativo', 'imagem',)
        }),
        ('Opções Avançadas', {
            'classes': ('collapse',),
            'fields': ('tamanho', 'peso'),
        }),
    )

# Customizando a administração do modelo Grupo
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# Customizando a administração do modelo Familia
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# Customizando a administração do modelo Colecao
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# Customizando a administração do modelo Localidade
class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# Customizando a administração dos modelos do carrinho
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'finalizado', 'criado_em', 'modificado', 'ativo', 'representante', 'formasrecebimento')
    list_filter = ('finalizado', 'ativo', 'representante')


class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrinho', 'produto', 'quantidade')


class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_compra', 'peso_total', 'representante', 'formasrecebimento')
    list_filter = ('data_compra', 'ativo', 'representante')


class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'compra', 'produto', 'quantidade',)


class FormasRecebimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao')



admin.site.register(Carrinho, CarrinhoAdmin)
admin.site.register(ItemCarrinho, ItemCarrinhoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(ItemCompra, ItemCompraAdmin)
admin.site.register(Representante)
admin.site.register(FormasRecebimento, FormasRecebimentoAdmin)
admin.site.register(Localidade, LocalidadeAdmin)
admin.site.register(Colecao, ColecaoAdmin)
admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Produtos, ProdutosAdmin)



custom_admin_site.register(Carrinho, CarrinhoAdmin)
custom_admin_site.register(ItemCarrinho, ItemCarrinhoAdmin)
custom_admin_site.register(Compra, CompraAdmin)
custom_admin_site.register(ItemCompra, ItemCompraAdmin)
custom_admin_site.register(Representante)
custom_admin_site.register(FormasRecebimento, FormasRecebimentoAdmin)
custom_admin_site.register(Localidade, LocalidadeAdmin)
custom_admin_site.register(Colecao, ColecaoAdmin)
custom_admin_site.register(Familia, FamiliaAdmin)
custom_admin_site.register(Grupo, GrupoAdmin)
custom_admin_site.register(Produtos, ProdutosAdmin)

