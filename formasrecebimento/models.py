from django.db import models

class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class FormasRecebimento(Base):
    descricao = models.CharField('Descrição',max_length=100)
    

    def __str__(self):
        return self.descricao
    
    class Meta:
        verbose_name = 'FormasRecebimento'
        verbose_name_plural = 'FormasRecebimento'