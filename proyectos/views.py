from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *
from kanban.models import *
from django.http import Http404
from rest_framework import status

# Create your views here.


class ProyectosListaAPIView(APIView):

    def get(self, request):
        equipos = Equipo.objects.filter(usuario=self.request.user)
        proyectos = Proyecto.objects.all()
        serializer = ProyectoSerializer(proyectos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProyectoSerializer(data=request.data)
        serializer.initial_data['autor'] = self.request.user.id
        if serializer.is_valid():
            serializer.save()
            configurarKanban(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProyectoApiView(APIView):

    def get_object(self, pk):
        try:
            return Proyecto.objects.get(pk=pk)
        except Proyecto.DoesNotExist:
            raise Http404

    def get(self, request, proyecto_id):
        snippet = self.get_object(proyecto_id)
        serializer = ProyectoSerializer(snippet)
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

    def patch(self):
        pass

    def delete(self):
        pass

class ListasKanbanListAPIView(APIView):

    def get(self, request, sprint_id):
        listas =  ListaKanban.objects.filter(sprint_id=sprint_id, fijar_en_kanban=True).order_by('orden')
        serializers = ListasKanbanSerializar(listas, many=True)
        return Response(serializers.data)
    
    def post(self, request, sprint_id):
        pass


class EquipoKanbanAPIListView(APIView):

    def get_sprint(self, pk):
        try:
            return Sprint.objects.get(pk=pk)
        except Sprint.DoesNotExist:
            raise Http404

    def get(self, request, sprint_id):
        sprint = self.get_sprint(sprint_id)
        equipo = Equipo.objects.filter(proyecto=sprint.proyecto)
        serializers = EquipoSerializer(equipo, many=True)
        return Response(serializers.data)

    def post(self, request, sprint_id):
        pass


class EquipoProyectoListApiView(APIView):

    def get(self, request, proyecto_id):
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


def configurarKanban(proyecto):
    equipo = Equipo()
    equipo.proyecto = proyecto
    equipo.usuario = proyecto.autor
    equipo.rol = Rol.objects.get(clave="administrador")
    equipo.usuario_registra = proyecto.autor
    equipo.save()

    sprint = Sprint()
    sprint.proyecto = proyecto
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
    lista_sin_priorizar.autor = proyecto.autor
    lista_sin_priorizar.save()

    lista_por_hacer = ListaKanban()
    lista_por_hacer.sprint = sprint
    lista_por_hacer.nombre = "Por hacer"
    lista_por_hacer.estatus = Estatus.objects.get(clave='porhacer')
    lista_por_hacer.orden = 2
    lista_por_hacer.autor = proyecto.autor
    lista_por_hacer.save()

    lista_haciendo = ListaKanban()
    lista_haciendo.sprint = sprint
    lista_haciendo.nombre = "Haciendo"
    lista_haciendo.estatus = Estatus.objects.get(clave='haciendo')
    lista_haciendo.orden = 3
    lista_haciendo.autor = proyecto.autor
    lista_haciendo.save()

    lista_pruebas = ListaKanban()
    lista_pruebas.sprint = sprint
    lista_pruebas.nombre = "Pruebas"
    lista_pruebas.estatus = Estatus.objects.get(clave='enpruebas')
    lista_pruebas.orden = 4
    lista_pruebas.autor = proyecto.autor
    lista_pruebas.save()

    lista_hecho = ListaKanban()
    lista_hecho.sprint = sprint
    lista_hecho.nombre = "Hecho"
    lista_hecho.estatus = Estatus.objects.get(clave='hecho')
    lista_hecho.orden = 5
    lista_hecho.autor = proyecto.autor
    lista_hecho.save()

    lista_archivado = ListaKanban()
    lista_archivado.sprint = sprint
    lista_archivado.nombre = "Archivado"
    lista_archivado.estatus = Estatus.objects.get(clave='archivado')
    lista_archivado.orden = 6
    lista_archivado.fijar_en_kanban = False
    lista_archivado.autor = proyecto.autor
    lista_archivado.save()