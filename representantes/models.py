from django.db import models

class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Representante(Base):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    regiao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
