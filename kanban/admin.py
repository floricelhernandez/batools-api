from django.contrib import admin
from kanban.models import *

# Register your models here.
admin.site.register(Sprint)
admin.site.register(Prioridad)
admin.site.register(ListaKanban)
admin.site.register(Tarea)
admin.site.register(Adjunto)
admin.site.register(Comentario)
admin.site.register(Asignacion)
admin.site.register(TipoTarea)
