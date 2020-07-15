from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/listas/', views.KanbanAPIView.as_view(), name='kanban'),
    path('<int:sprint_id>/kanban/movimiento', views.TareaApiView.as_view(), name='movimiento'),
    path('tarea/adjunto', views.AdjuntosApiView.as_view(), name='adjunto'),
    path('tarea/comentario', views.ComentariosApiView.as_view(), name='comentario'),
    path('tarea/asignacion', views.AsignacionApiView.as_view(), name='asignacion'),
] 