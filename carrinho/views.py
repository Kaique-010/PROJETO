# carrinho/views.py

import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Carrinho, ItemCarrinho, Compra, ItemCompra
from produtos.models import Produtos
from decimal import Decimal
from django.contrib import messages
from django.core.mail import send_mail
import requests
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user, finalizado=False)
    item, item_created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    
    if item_created:
        item.quantidade = quantidade
    else:
        item.quantidade += quantidade
    
    item.save()
    
    return redirect('produtos_list')

@login_required
def carrinho_detalhe(request):
    api_key = "goldapi-141hslyhvp7qw-io"
    symbol = "XAU"
    curr = "USD"
    
    url = f"https://www.goldapi.io/api/{symbol}/{curr}"
    
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    def make_gapi_request():
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lança HTTPError para respostas ruins
            data = response.json()
            return Decimal(data['price'])
        except requests.exceptions.RequestException as e:
            # Tratar exceções de requisição como erros de conexão ou timeout
            print(f"Erro ao buscar preço do ouro: {e}")
            return None
        except (KeyError, ValueError) as e:
            # Tratar erros de parsing JSON ou chave 'price' ausente
            print(f"Erro ao analisar dados de preço do ouro: {e}")
            return None

    # Chamada à função para obter o preço do ouro
    gold_price_per_gram = make_gapi_request()

    if gold_price_per_gram is not None:
        # Limitar as casas decimais a 3
        gold_price_per_gram = gold_price_per_gram.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

    # Obter o carrinho do usuário e calcular totais
    carrinho = Carrinho.objects.filter(usuario=request.user, finalizado=False).first()
    total_quantidade = Decimal('0')
    total_peso = Decimal('0')
    produtos_comprados = []

    if carrinho:
        for item in carrinho.itens.all():
            quantidade = item.quantidade
            peso = item.produto.peso

            total_quantidade += Decimal(quantidade)
            total_peso += Decimal(peso) * Decimal(quantidade)
            produtos_comprados.append({
                'nome': item.produto.nome,
                'quantidade': quantidade,
                'peso': peso
            })

    # Obter histórico de compras do usuário
    compras = Compra.objects.filter(usuario=request.user).order_by('-data_compra')

    # Preparar contexto para renderizar o template
    context = {
        'carrinho': carrinho,
        'total_quantidade': total_quantidade,
        'total_peso': total_peso,
        'compras': compras,
        'produtos_comprados': produtos_comprados,
        'gold_price_per_gram': gold_price_per_gram,
    }

    return render(request, 'carrinho_detalhe.html', context)

@login_required
def checkout(request):
    produtos_no_carrinho = ItemCarrinho.objects.filter(carrinho__usuario=request.user, carrinho__finalizado=False)
    total_peso = sum(item.produto.peso * item.quantidade for item in produtos_no_carrinho)
    contexto = {
        'produtos': produtos_no_carrinho,
        'total_peso': total_peso,
    }
    return render(request, 'carrinho/checkout.html', contexto)

@login_required
def completar_compra(request):
    if request.method == 'POST':
        try:
            carrinho = get_object_or_404(Carrinho, usuario=request.user, finalizado=False)
        except Carrinho.DoesNotExist:
            return HttpResponse("Carrinho não encontrado ou já finalizado.", status=404)

        total_quantidade = Decimal('0')
        total_peso = Decimal('0')

        for item in carrinho.itens.all():
            total_quantidade += Decimal(item.quantidade)
            total_peso += Decimal(item.produto.peso) * Decimal(item.quantidade)

        forma_recebimento = request.POST.get('forma_recebimento')

        # Verifique se a forma de recebimento está sendo capturada corretamente
        if not forma_recebimento:
            return HttpResponse("Forma de recebimento não fornecida.", status=400)

        # Cria a compra e salva a forma de recebimento
        compra = Compra.objects.create(
            usuario=request.user,
            peso_total=total_peso,
            forma_recebimento=forma_recebimento  # Salvar forma de recebimento
        )

        carrinho.finalizado = True
        carrinho.save()

        for item in carrinho.itens.all():
            ItemCompra.objects.create(
                compra=compra,
                produto=item.produto,
                quantidade=item.quantidade
            )

        nome = request.POST.get('nome')
        email = request.POST.get('email')

        produtos_comprados = "\n".join([
            f"{item.produto.nome} - {item.quantidade} unidades, {item.produto.peso} gramas cada"
            for item in carrinho.itens.all()
        ])

        email_destinatarios = ['leo.kaique.010@gmail.com', 'antonio@joalheriasgravina.com.br']
        email_destinatarios.append(email)

        assunto = 'Detalhes do Pedido'
        mensagem = (f"Nome: {nome}\n"
                    f"Email: {email}\n\n"
                    f"Total de Itens: {total_quantidade}\n"
                    f"Peso Total: {total_peso} gr\n\n"
                    f"Forma de Recebimento: {compra.forma_recebimento}\n\n"
                    f"Produtos Comprados:\n{produtos_comprados}")

        try:
            send_mail(assunto, mensagem, settings.EMAIL_HOST_USER, email_destinatarios)
        except Exception as e:
            return HttpResponse(f'Erro ao enviar e-mail: {e}')

        return render(request, 'carrinho/compra_concluida.html', {
            'total_quantidade': total_quantidade,
            'total_peso': total_peso,
            'produtos_comprados': carrinho.itens.all()
        })

    return render(request, 'carrinho/completar_compra.html')

@login_required
def limpar_carrinho(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user, finalizado=False)
    carrinho.itens.all().delete()
    return redirect("carrinho:carrinho_detalhe")

@login_required
def historico_compras(request):
    historico = Compra.objects.filter(usuario=request.user).prefetch_related('itens__produto')
    compras_com_forma = []
    
    for compra in historico:
        compras_com_forma.append({
            'id': compra.id,
            'criado_em': compra.data_compra,
            'peso_total': compra.calcular_peso_total(),
            'forma_recebimento': compra.forma_recebimento,  # Acesse o atributo diretamente
            'itens': compra.itens.all()
        })
    
    return render(request, 'historico_compras.html', {'historico': compras_com_forma})
