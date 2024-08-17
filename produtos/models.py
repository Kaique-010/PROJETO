from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from stdimage import StdImageField
from django.utils.html import mark_safe

# Modelo base para adicionar campos comuns a todos os modelos que o herdam
class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)  # Data de criação automática
    modificado = models.DateTimeField('Data de Modificação', auto_now=True)  # Data de modificação automática
    ativo = models.BooleanField('Ativo?', default=True)  # Indicador de ativo/inativo

    class Meta:
        abstract = True  # Define o modelo como abstrato (não cria tabela no banco de dados)

# Modelo para Família de Produtos
class Familia(models.Model):
    nome = models.CharField('Nome', max_length=50)  # Nome da família

    def __str__(self):
        return self.nome  # Representação em string do modelo

    class Meta:
        verbose_name = 'Família'  # Nome singular no admin
        verbose_name_plural = 'Famílias'  # Nome plural no admin

# Modelo para Coleção de Produtos
class Colecao(models.Model):
    nome = models.CharField('Nome', max_length=50)  # Nome da coleção

    def __str__(self):
        return self.nome  # Representação em string do modelo

    class Meta:
        verbose_name = 'Coleção'  # Nome singular no admin
        verbose_name_plural = 'Coleções'  # Nome plural no admin

# Modelo para Grupo de Produtos
class Grupo(models.Model):
    nome = models.CharField('Nome', max_length=50)  # Nome do grupo
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumbnail': (90, 90)}, blank=True, null=True)
    descricao = models.TextField('Descrição', max_length=100,blank=True, null=True)

    def __str__(self):
        return self.nome  # Representação em string do modelo
    
    def imagem_tag(self):
        try:
            return mark_safe(f'<img src="{self.imagem.url}" width="80" height="80" />')
        except AttributeError:
            return "No Image"

    imagem_tag.short_description = 'Imagem'

    def save(self, *args, **kwargs):
        if not self.imagem:
            self.imagem = DEFAULT_IMAGE_PATH  # Define a imagem padrão
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Grupo'  # Nome singular no admin
        verbose_name_plural = 'Grupos'  # Nome plural no admin

# Modelo para Origem de Produtos
class Origem(models.Model):
    nome = models.CharField('Nome', max_length=50)  # Nome da origem

    def __str__(self):
        return self.nome  # Representação em string do modelo

    class Meta:
        verbose_name = 'Origem'  # Nome singular no admin
        verbose_name_plural = 'Origens'  # Nome plural no admin

# Modelo para Localidade de Produtos
class Localidade(models.Model):
    nome = models.CharField('Nome', max_length=50)  # Nome da localidade

    def __str__(self):
        return self.nome  # Representação em string do modelo

    class Meta:
        verbose_name = 'Localidade'  # Nome singular no admin
        verbose_name_plural = 'Localidades'  # Nome plural no admin

# Modelo para Produtos, herdando de Base
# Caminho para a imagem padrão
DEFAULT_IMAGE_PATH = 'path/to/default/image.jpg'

class Produtos(Base):
    nome = models.CharField('Nome', max_length=50)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, blank=True, null=True)
    descricao = models.CharField('Descrição', max_length=100, blank=True, null=True)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, blank=True, null=True)
    colecao = models.ForeignKey(Colecao, on_delete=models.CASCADE, blank=True, null=True, default=None)
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumbnail': (90, 90)}, blank=False, null=False)
    tamanho = models.CharField('Tamanho', max_length=10, blank=True, null=True)
    peso = models.DecimalField('Peso (em gramas)', max_digits=6, decimal_places=2, blank=False, null=False)
    quantidade = models.IntegerField('Quantidade', default=1)

    def __str__(self):
        return self.nome

    def imagem_tag(self):
        try:
            return mark_safe(f'<img src="{self.imagem.url}" width="80" height="80" />')
        except AttributeError:
            return "No Image"

    imagem_tag.short_description = 'Imagem'

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):
        if not self.imagem:
            self.imagem = DEFAULT_IMAGE_PATH  # Define a imagem padrão
        super().save(*args, **kwargs)