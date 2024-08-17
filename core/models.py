from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validator import validate_cnpj
from representantes.models import Representante

class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class LoginManager(BaseUserManager):
    def create_user(self, email, cnpj, password=None, representante=None, cep=None):
        if not email:
            raise ValueError('O usuário precisa de um email')
   
        if cnpj is not None and not validate_cnpj(cnpj):
            raise ValueError('O usuário precisa de um CNPJ válido')
        user = self.model(email=self.normalize_email(email), cnpj=cnpj, representante=Representante, cep=cep)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, None, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Login(AbstractBaseUser, Base):
    email = models.EmailField(unique=True)
    cnpj = models.CharField(max_length=18, validators=[validate_cnpj], blank=True, null=True)
    representante = models.ForeignKey(Representante, on_delete=models.SET_NULL, null=True, blank=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = LoginManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
