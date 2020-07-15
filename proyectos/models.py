from django.db import models
from usuarios.models import *
from django.contrib.auth.models import User

# Create your models here.


class Categoria (models.Model):
    nombre = models.TextField(max_length=25)
    clave = models.TextField(max_length=25)
    descripcion = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "categorias"


class Proyecto (models.Model):
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField()
    slack_bot_token = models.TextField(max_length=1500, null=True, blank=True)
    slack_channel_id = models.TextField(max_length=1500, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    def sprints(self):
        return Sprint.objects.filter(proyecto_id=self.id)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "proyectos"


class Rol (models.Model):
    descripcion = models.TextField(max_length=50)
    clave = models.TextField(max_length=50)
    rol_del_sistema = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = "roles"


class Equipo(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='participante')
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    usuario_registra = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.proyecto.nombre + " - " +self.usuario.username

    class Meta:
        db_table = "proyectos_equipos"
        unique_together = ('proyecto', 'usuario')


class Estatus (models.Model):
    descripcion = models.TextField(max_length=25)
    clave = models.TextField(max_length=25)

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = "estatus"


class Sprint (models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    descripcion = models.TextField()
    no_sprint = models.SmallIntegerField(default=1)
    dias_sprint = models.SmallIntegerField(default=15)
    inicio = models.DateField(blank=True, null=True)
    fin = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.proyecto.nombre + " " + str(self.no_sprint)

    class Meta:
        db_table = "sprints"