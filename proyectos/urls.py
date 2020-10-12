from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProyectosListaAPIView.as_view(), name='proyectos'),
    path('<int:proyecto_id>/', views.ProyectoApiView.as_view(), name='proyecto'),
    path('<int:proyecto_id>/equipos', views.ProyectoApiView.as_view(), name='proyecto-equipo'),
    path('sprints/<int:sprint_id>/kanban', views.ListasKanbanListAPIView.as_view(), name='kanban'),
    path('sprints/<int:sprint_id>/kanban/equipo', views.EquipoKanbanAPIListView.as_view(), name='kanban-equipo'),

]