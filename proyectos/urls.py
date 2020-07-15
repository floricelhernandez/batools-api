from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProyectosListaAPIView.as_view(), name='api-proyecto'),
    path('<int:pk>/', views.ProyectoApiView.as_view(), name='api-proyecto-detalle'),
]