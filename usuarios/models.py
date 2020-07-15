from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from usuarios.managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.FileField(blank=True, null=True, upload_to='avatar')
    slack_id = models.TextField(max_length=250, blank=True, null=True)
    recibir_correos = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

    class Meta:
        db_table = "usuarios_perfiles"



