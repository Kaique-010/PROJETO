from django.contrib import admin
from .models import Produtos, Grupo, Familia, Colecao, Localidade
from .forms import ProdutosAdminForm
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "ACG"
    site_title = "Administração ACG"
    index_title = "Bem-vindo à Administração"

custom_admin_site = CustomAdminSite(name='custom_admin')

# Customizando a administração do modelo Produtos
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo', 'familia', 'colecao', 'ativo', 'imagem_tag', 'id')  # Campos exibidos na lista de produtos
    list_filter = ('grupo', 'familia', 'colecao', 'ativo')  # Filtros disponíveis na barra lateral
    search_fields = ('nome', 'descricao')  # Campos pesquisáveis
    readonly_fields = ('imagem_tag',)  # Campos somente leitura
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'grupo', 'familia', 'colecao', 'ativo', 'imagem',)
        }),
        ('Opções Avançadas', {
            'classes': ('collapse',),
            'fields': ('tamanho', 'peso'),
        }),
    )

# Registrando o modelo Produtos com a configuração customizada
custom_admin_site.register(Produtos, ProdutosAdmin)
admin.site.register(Produtos, ProdutosAdmin)

# Customizando a administração do modelo Grupo
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Registrando o modelo Grupo com a configuração customizada
custom_admin_site.register(Grupo, GrupoAdmin)
admin.site.register(Grupo, GrupoAdmin)

# Customizando a administração do modelo Familia
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Registrando o modelo Familia com a configuração customizada
custom_admin_site.register(Familia, FamiliaAdmin)
admin.site.register(Familia, FamiliaAdmin)

# Customizando a administração do modelo Colecao
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Registrando o modelo Colecao com a configuração customizada
custom_admin_site.register(Colecao, ColecaoAdmin)
admin.site.register(Colecao, ColecaoAdmin)

# Customizando a administração do modelo Localidade
class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Registrando o modelo Localidade com a configuração customizada
custom_admin_site.register(Localidade, LocalidadeAdmin)
admin.site.register(Localidade, LocalidadeAdmin)
