"""batools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kanban import views as kviews
from proyectos import views as pviews
from tickets import views as tviews
from usuarios import views as uviews
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

urlpatterns = [

    # Proyectos
    path('', pviews.IndexView.as_view(), name='inicio'),
    path('proyecto/<int:proyecto_id>/configuracion/', pviews.ConfiguracionProyectoView.as_view(), name='proyecto-configuracion'),
    path('proyecto/<int:proyecto_id>/', pviews.ProyectoView.as_view(), name='proyecto'),
    path('proyecto/<int:proyecto_id>/equipo/', pviews.EquipoProyectoApiView.as_view(), name='proyecto-equipo'),
    path('proyecto/equipo', pviews.EquipoProyectoApiView.as_view(), name='equipo'),


    # Usuarios y autenticación
    path('accounts/', include('allauth.urls')), # new


    #Kanban
    path('<int:sprint_id>/kanban/', kviews.KanbanView.as_view(), name='app-kanban'),
    path('<int:sprint_id>/kanban/movimiento', kviews.TareaApiView.as_view(), name='movimiento'),
    path('kanban/tarea/adjunto', kviews.AdjuntosApiView.as_view(), name='adjunto'),
    path('kanban/tarea/comentario', kviews.ComentariosApiView.as_view(), name='comentario'),
    path('kanban/tarea/asignacion', kviews.AsignacionApiView.as_view(), name='asignacion'),

    # Ticktes
    path('tickets/', tviews.TicketsView.as_view(), name='app-tickets'),
    path('tickets/api', tviews.TicketApiView.as_view(), name='tickets'),

    # Equipo


    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
