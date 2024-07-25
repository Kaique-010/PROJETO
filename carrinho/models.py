from django.db import models
from conecta import settings
from produtos.models import Produtos
from django.utils import timezone

class Base(models.Model):
    criado = models.DateField('Data de Criação', default=timezone.now)
    modificado = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class FormasRecebimento(models.Model):
    DINHEIRO = 'dinheiro'
    PIX = 'pix'
    DEPOSITO = 'deposito'
    DEBITO = 'cartao_debito'
    CREDITO = 'cartao_credito'
    BOLETO = 'boleto'

    FORMAS_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (PIX, 'Pix'),
        (DEPOSITO, 'Deposito'),
        (DEBITO, 'Cartão de Débito'),
        (CREDITO, 'Cartão de Crédito'),
        (BOLETO, 'Boleto')
    ]

    forma = models.CharField(max_length=20, choices=FORMAS_CHOICES)

    def __str__(self):
        return self.get_forma_display()

class Carrinho(Base):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finalizado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    forma_recebimento = models.CharField(max_length=20, choices=FormasRecebimento.FORMAS_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'Carrinho do {self.usuario.username} - {"Finalizado" if self.finalizado else "Aberto"}'

    def get_peso_total(self):
        peso_total = 0
        for item in self.itens.all():
            peso_total += item.produto.peso * item.quantidade
        return peso_total

class ItemCarrinho(Base):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'

    @property
    def peso_total(self):
        return self.produto.peso * self.quantidade

class Compra(Base):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    peso_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_recebimento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Compra de {self.usuario.username} em {self.data_compra}'

    def calcular_peso_total(self):
        peso_total = 0
        for item in self.itens.all():
            peso_total += item.produto.peso * item.quantidade
        self.peso_total = peso_total
        self.save()
        return peso_total

class ItemCompra(Base):
    compra = models.ForeignKey(Compra, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'

    @property
    def peso_total(self):
        return self.produto.peso * self.quantidade
