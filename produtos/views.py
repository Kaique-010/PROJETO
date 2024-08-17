from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Colecao, Produtos, Grupo
from .forms import ProdutosModelForm, ProdutoFilterForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template


class ProdutosListView(ListView):
    model = Produtos
    template_name = 'produtos/produtos_list.html'
    context_object_name = 'produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProdutoFilterForm(self.request.GET)
        context['grupos'] = Grupo.objects.all()

        grupo_id = self.request.GET.get('grupo')
        if grupo_id:
            context['grupo_selecionado'] = get_object_or_404(Grupo, pk=grupo_id)
        else:
            context['grupo_selecionado'] = None

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProdutoFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('colecao'):
                queryset = queryset.filter(colecao=form.cleaned_data['colecao'])
            if form.cleaned_data.get('familia'):
                queryset = queryset.filter(familia=form.cleaned_data['familia'])
            if form.cleaned_data.get('ativo') is not None:
                queryset = queryset.filter(ativo=form.cleaned_data['ativo'])
            if form.cleaned_data.get('grupo'):
                queryset = queryset.filter(grupo=form.cleaned_data['grupo'])
        return queryset

class ProdutosCreateView(CreateView):
    model = Produtos
    form_class = ProdutosModelForm
    template_name = 'produtos/produtos_create.html'
    success_url = reverse_lazy('produtos_list')

class ProdutosUpdateView(UpdateView):
    model = Produtos
    form_class = ProdutosModelForm
    template_name = 'produtos/produtos_create.html'
    success_url = reverse_lazy('produtos_list')

class ProdutoDetailView(DetailView):
    model = Produtos
    template_name = 'produtos/produto_detalhe.html'
    context_object_name = 'produto'

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = 'produtos/grupo_detalhe.html'
    context_object_name = 'grupo'

def produtos_create(request):
    if request.method == 'POST':
        form = ProdutosModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produtos_list')
    else:
        form = ProdutosModelForm()
    return render(request, 'produtos/produtos_create.html', {'form': form})

def produtos_list(request):
    grupo_id = request.GET.get('grupo')
    if grupo_id:
        grupo_selecionado = get_object_or_404(Grupo, id=grupo_id)
        produtos = Produtos.objects.filter(grupo=grupo_selecionado)
    else:
        produtos = Produtos.objects.all()
        grupo_selecionado = None

    grupos = Grupo.objects.all()
    return render(request, 'produtos/produtos_list.html', {
        'produtos': produtos,
        'grupos': grupos,
        'grupo_selecionado': grupo_selecionado,
        'form': ProdutoFilterForm(request.GET),
    })

class GrupoListView(ListView):
    model = Grupo
    template_name = 'produtos/grupo_list.html'
    context_object_name = 'grupos'

class GrupoProdutosView(ListView):
    model = Produtos
    template_name = 'produtos/grupo_produtos.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        grupo_id = self.kwargs.get('grupo_id')
        return Produtos.objects.filter(grupo_id=grupo_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo_id = self.kwargs.get('grupo_id')
        context['grupo'] = get_object_or_404(Grupo, pk=grupo_id)
        return context
    
def filtrar_produtos(request):
    grupo = request.GET.get('grupo')
    familia = request.GET.get('familia')
    colecao = request.GET.get('colecao')
    ativo = request.GET.get('ativo')

    produtos = Produtos.objects.all()

    if grupo:
        produtos = produtos.filter(grupo=grupo)
    if familia:
        produtos = produtos.filter(familia=familia)
    if colecao:
        produtos = produtos.filter(colecao=colecao)
    if ativo:
        produtos = produtos.filter(ativo=(ativo == 'true'))

    for produto in produtos:
        if not produto.imagem:
            produto.imagem_url = 'Sem Imagem' 
        else:
            produto.imagem_url = produto.imagem.url

    context = {
        'produtos': produtos,
    }

    return render(request, 'produtos/produtos_lista_parcial.html', context)

def colecao(request):
    colecoes = Colecao.objects.all() 
    return render(request, 'produtos/produtos_list.html', {'colecoes': colecoes})
