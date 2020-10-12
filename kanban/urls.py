from django.urls import path
from . import views

urlpatterns = [
    path('listas/<int:lista_id>/tareas', views.ListaTareasApiView.as_view(), name='lista-tareas'),
    path('tareas/<int:tarea_id>', views.TareaApiView.as_view(), name='tarea'),
    path('tareas/<int:tarea_id>/reorden', views.ReordenarTareaApiView.as_view(), name='tarea'),
    path('tareas/<int:tarea_id>/adjuntos', views.AdjuntosApiView.as_view(), name='lista-adjuntos'),
    path('tareas/<int:tarea_id>/adjuntos/<int:adjunto_id>', views.AdjuntosApiView.as_view(), name='adjunto'),
    path('tareas/<int:tarea_id>/comentarios', views.ComentariosApiView.as_view(), name='lista-comentarios'),
    path('tareas/<int:tarea_id>/comentarios/<int:comentario_id>', views.ComentariosApiView.as_view(), name='comentario'),
    path('tareas/<int:tarea_id>/asignaciones', views.AsignacionListApiView.as_view(), name='lista-asignaciones'),
    path('tareas/<int:tarea_id>/asignaciones/<int:asignacion_id>', views.AsignacionApiView.as_view(), name='asignacion'),
] 