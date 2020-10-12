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
from tickets import views as tviews
from usuarios import views as uviews
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    path('api/token/', uviews.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Proyectos

    #path('proyecto/<int:proyecto_id>/configuracion/', pviews.ConfiguracionProyectoView.as_view(), name='proyecto-configuracion'),
    #path('proyecto/<int:proyecto_id>/equipo/', pviews.EquipoProyectoApiView.as_view(), name='proyecto-equipo'),
    #path('proyecto/equipo', pviews.EquipoProyectoApiView.as_view(), name='equipo'),


    # Usuarios y autenticación


    #Kanban


    # Ticktes
    path('tickets/', tviews.TicketsView.as_view(), name='app-tickets'),
    path('tickets/api', tviews.TicketApiView.as_view(), name='tickets'),

    # Equipo

    path('api/proyectos/', include('proyectos.urls')),
    path('api/kanban/', include('kanban.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
