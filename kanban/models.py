from django.db import models
from django.contrib.auth.models import User
from proyectos.models import *
from usuarios.models import *

# Create your models here.


class Prioridad (models.Model):
    nombre = models.TextField(max_length=25)
    descripcion = models.TextField(max_length=50)
    clave = models.TextField(max_length=25, default='ninguno')
    orden = models.SmallIntegerField(default=1)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "prioridades"


class ListaKanban (models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.PROTECT)
    nombre = models.TextField(max_length=35)
    estatus = models.ForeignKey(Estatus, on_delete=models.PROTECT, default=1)
    col_pila_sin_priorizar = models.BooleanField(default=False)
    col_finalizado = models.BooleanField(default=False)
    color = models.TextField(max_length=8)
    orden = models.PositiveSmallIntegerField(default=1)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    def tareas(self):
        return Tarea.objects.filter(lista_kanban_id=self.id).order_by('orden')

    def __str__(self):
        return self.nombre + " " + self.sprint.proyecto.nombre + "("+str(self.sprint.no_sprint)+")"

    class Meta:
        db_table = "listas_kanban"


class Tarea (models.Model):
    lista_kanban = models.ForeignKey(ListaKanban, on_delete=models.PROTECT, blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.PROTECT, blank=True, null=True)
    estatus = models.ForeignKey(Estatus, on_delete=models.PROTECT, default=1)
    orden = models.PositiveSmallIntegerField(default=1)
    no_tarea = models.IntegerField(default=1)
    nombre = models.TextField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    vencimiento = models.DateField(null=True, blank=True)
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.orden) + " (" + self.lista_kanban.nombre+")"

    @property
    def adjuntos(self):
        return Adjunto.objects.filter(tarea_id=self.id)

    @property
    def asignaciones(self):
        return Asignacion.objects.filter(tarea_id=self.id, activo=True)

    class Meta:
        db_table = "tareas"


class Asignacion(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='participante_asignado')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_asigna = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def perfil(self):
        return Perfil.objects.get(usuario_id=self.usuario.id)

    def __str__(self):
        return self.usuario.username + " (" + self.tarea.nombre+")"

    class Meta:
        db_table = "tareas_asignaciones"


class Adjunto (models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT, related_name='adjuntos')
    comentario = models.TextField(blank=True, null=True, max_length=200)
    nombre_archivo = models.TextField(blank=True, null=True, max_length=200)
    ruta = models.TextField(max_length=1000, blank=True, null=True)
    archivo = models.FileField()
    tipo = models.TextField(max_length=25, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "Tarea" + str(self.tarea.id)

    class Meta:
        db_table = "tareas_adjuntos"


class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT, related_name='comentarios')
    comentario = models.TextField(max_length=500)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = "tareas_comentarios"
