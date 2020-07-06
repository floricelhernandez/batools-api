from django.views import generic
from proyectos.models import *
from django import forms
from django.shortcuts import render

from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.http import JsonResponse
from .serializers import *
from kanban.models import *

# Create your views here.


class ProyectoForm(forms.ModelForm):
    nombre = forms.CharField(widget= forms.TextInput
                           (attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.Textarea
                            (attrs={'class': 'form-control', "rows": 9}))
    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion',)



class IndexView(LoginRequiredMixin, generic.View):

    def get(self, request):
        form = ProyectoForm()
        equipos = Equipo.objects.filter(usuario=self.request.user)
        return render(request, 'kanban/proyectos.html', {'form': form, 'proyectos': equipos})

    @transaction.atomic()
    def post(self, request):
        proyecto = ProyectoForm(request.POST)
        proyecto.instance.autor = self.request.user
        proyecto.save()
        form = ProyectoForm()

        equipo = Equipo()
        equipo.proyecto = proyecto.instance
        equipo.usuario = self.request.user
        equipo.rol= Rol.objects.get(clave= "administrador")
        equipo.usuario_registra = self.request.user
        equipo.save()

        sprint = Sprint()
        sprint.proyecto= proyecto.instance
        sprint.descripcion = "Sprint 1"
        sprint.no_sprint = 1
        sprint.dias_sprint = 15
        sprint.save()

        lista_sin_priorizar = ListaKanban()
        lista_sin_priorizar.sprint = sprint
        lista_sin_priorizar.nombre = "Sin priorizar"
        lista_sin_priorizar.estatus = Estatus.objects.get(clave='sinpriorizar')
        lista_sin_priorizar.orden = 1
        lista_sin_priorizar.fijar_en_kanban = False
        lista_sin_priorizar.autor = self.request.user
        lista_sin_priorizar.save()

        lista_por_hacer = ListaKanban()
        lista_por_hacer.sprint = sprint
        lista_por_hacer.nombre = "Por hacer"
        lista_por_hacer.estatus = Estatus.objects.get(clave='porhacer')
        lista_por_hacer.orden = 2
        lista_por_hacer.autor = self.request.user
        lista_por_hacer.save()

        lista_haciendo = ListaKanban()
        lista_haciendo.sprint = sprint
        lista_haciendo.nombre = "Haciendo"
        lista_haciendo.estatus = Estatus.objects.get(clave='haciendo')
        lista_haciendo.orden = 3
        lista_haciendo.autor = self.request.user
        lista_haciendo.save()

        lista_pruebas = ListaKanban()
        lista_pruebas.sprint = sprint
        lista_pruebas.nombre = "Pruebas"
        lista_pruebas.estatus = Estatus.objects.get(clave='enpruebas')
        lista_pruebas.orden = 4
        lista_pruebas.autor = self.request.user
        lista_pruebas.save()

        lista_hecho = ListaKanban()
        lista_hecho.sprint = sprint
        lista_hecho.nombre = "Hecho"
        lista_hecho.estatus = Estatus.objects.get(clave='hecho')
        lista_hecho.orden = 5
        lista_hecho.autor = self.request.user
        lista_hecho.save()

        lista_archivado = ListaKanban()
        lista_archivado.sprint = sprint
        lista_archivado.nombre = "Archivado"
        lista_archivado.estatus = Estatus.objects.get(clave='archivado')
        lista_archivado.orden = 6
        lista_archivado.fijar_en_kanban = False
        lista_archivado.autor = self.request.user
        lista_archivado.save()

        equipos = Equipo.objects.filter(usuario=self.request.user)
        return render(request, 'kanban/proyectos.html', {'form': form, 'proyectos': equipos})


class ConfiguracionProyectoView(LoginRequiredMixin, generic.ListView):
    template_name = 'proyectos/configuracion.html'
    context_object_name = 'configuracion'

    def get_queryset(self):
        pass

    def get_context_data(self,**kwargs):
        context = super(ConfiguracionProyectoView, self).get_context_data(**kwargs)
        proyecto =  Proyecto.objects.get(id=self.kwargs['proyecto_id'])
        context['proyecto'] = proyecto
        context['equipo'] = Equipo.objects.filter(proyecto_id=proyecto.id)
        context['usuarios'] = User.objects.all()
        context['roles'] = Rol.objects.all()
        return context


class ProyectoView(APIView):

    def get(self, request, sprint_id):
        id_proyecto = request.GET['idProyecto']
        proyecto = Proyecto.objects.get(id=id_proyecto)
        serializer = ProyectoSerializer(proyecto)
        return Response(serializer.data)

    def put(self, request, proyecto_id):
        proyecto_json = request.POST
        proyecto= Proyecto.objects.get(id=proyecto_id)
        proyecto.nombre = proyecto_json['nombre']
        proyecto.descripcion = proyecto_json['descripcion']
        proyecto.slack_bot_token =  proyecto_json['slack_bot_token']
        proyecto.slack_channel_id = proyecto_json['slack_channel_id']
        proyecto.save()
        data = {
            'success': True,
        }
        return JsonResponse(data)

class EquipoProyectoApiView(APIView):

    def get(self, request):
        proyecto_id = request.GET['proyecto_id']
        equipo = Equipo.objects.filter(proyecto_id=proyecto_id)
        serializer = EquipoSerializer(equipo, many=True)
        return Response(serializer.data)

    def post(self, request, proyecto_id):
        equipo = Equipo()
        equipo.proyecto = Proyecto.objects.get(id=proyecto_id)
        equipo.usuario = User.objects.get(id=request.POST['usuario'])
        equipo.rol = Rol.objects.get(id=request.POST['rol'])
        equipo.usuario_registra = self.request.user
        equipo.save()
        data = {
            'success': True,
        }
        return JsonResponse(data)