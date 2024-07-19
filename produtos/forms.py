from django import forms
from .models import Produtos, Grupo, Colecao, Familia

# Formulário para o modelo de Produtos
class ProdutosModelForm(forms.ModelForm):
    class Meta:
        model = Produtos  # Define o modelo a ser utilizado pelo formulário
        fields = ['nome', 'descricao', 'grupo', 'familia', 'colecao', 'imagem', 'tamanho', 'peso', 'ativo']  # Campos incluídos no formulário

# Formulário para filtrar produtos
class ProdutoFilterForm(forms.Form):
    grupo = forms.ModelChoiceField(queryset=Produtos.objects.values_list('grupo', flat=True).distinct(), required=False)
    familia = forms.ModelChoiceField(queryset=Produtos.objects.values_list('familia', flat=True).distinct(), required=False)
    colecao = forms.ModelChoiceField(queryset=Produtos.objects.values_list('colecao', flat=True).distinct(), required=False)
    ativo = forms.BooleanField(required=False, label='Ativo')

# Formulário personalizado para administração de Produtos
class ProdutosAdminForm(forms.ModelForm):
    class Meta:
        model = Produtos
        exclude = ['slug']  # Exclui o campo 'slug' do formulário

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['readonly'] = True  # Define o campo 'slug' como somente leitura
