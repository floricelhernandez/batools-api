from django.views import generic
from kanban.models import *
from .tasks import *
from kanban.serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404



class ListaTareasApiView(APIView):

    def get_lista_kanban(self, pk):
        try:
            return ListaKanban.objects.get(pk=pk)
        except ListaKanban.DoesNotExist:
            raise Http404

    def get(self, request, lista_id):
        try:
            lista = self.get_lista_kanban(lista_id)
            tareas = Tarea.objects.filter(lista_kanban__id= lista.pk)
            serializer = TareaSerializer(tareas, many=True)
            return Response(serializer.data)
        except Http404 as http404:
            return Response({"error: No se encontró el ID de la lista propocionada"}, status= status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, lista_id):

        nombre = request.data['titulo']
        lista_kanban = self.get_lista_kanban(lista_id)
        tarea = Tarea()
        tarea.nombre = nombre
        tarea.no_tarea = Tarea.objects.filter(proyecto=lista_kanban.sprint.proyecto).count()+1
        tarea.lista_kanban= lista_kanban
        tarea.proyecto=tarea.lista_kanban.sprint.proyecto
        tarea.orden =1
        tarea.autor = self.request.user
        tarea.prioridad = Prioridad.objects.get(clave='ninguno')
        tareas = Tarea.objects.filter(lista_kanban_id=lista_kanban.id).order_by('orden')
        orden = 2

        for t in tareas:
            t.orden= orden
            orden= orden+1
            t.save()
        tarea.save()

        try:
            proyecto = Proyecto.objects.get(id=lista_kanban.sprint.proyecto.id)
            if proyecto.slack_bot_token:
                if proyecto.slack_channel_id:
                    send_slack_message(proyecto.slack_bot_token, proyecto.slack_channel_id, self.request.user.username + " ha creado la tarea: " + tarea.nombre)
        except Exception as ex:
            print(ex)

        serializer = TareaSerializer(tarea)
        return Response(serializer.data)


class TareaApiView(APIView):

    def get_tarea(self, pk):
        try:
            return Tarea.objects.get(pk=pk)
        except Tarea.DoesNotExist:
            raise Http404

    def get(self, request, tarea_id):
        tarea = self.get_tarea(tarea_id)
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request, sprint_id):
        tarea_json = json.loads(request.POST['tarea'])
        tarea= Tarea.objects.get(id=tarea_json['id'])
        try:
            tarea.prioridad = Prioridad.objects.get(id=tarea_json['prioridad'][0])
        except:
            tarea.prioridad = Prioridad.objects.get(id=tarea_json['prioridad']['id'])
        tarea.nombre = tarea_json['nombre']
        tarea.descripcion = tarea_json['descripcion']
        tarea.save()
        data = {
            'pk': "ok",
        }
        return JsonResponse(data)

    def patch(self, request, tarea_id):
        data=request.data
        tarea = self.get_tarea(tarea_id)
        tarea_serializer = TareaSerializer(tarea,data=data, partial=True)

        if tarea_serializer.is_valid():
            tarea_serializer.save()
            return Response(tarea_serializer.data, status=status.HTTP_200_OK)

        # return a meaningful error response
        return Response(tarea_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReordenarTareaApiView(APIView):

    def get_tarea(self, pk):
        try:
            return Tarea.objects.get(pk=pk)
        except Tarea.DoesNotExist:
            raise Http404

    def patch(self, request, tarea_id):
        data=request.data
        tarea = self.get_tarea(tarea_id)
        tarea_serializer = TareaSerializer(tarea,data=data, partial=True)

        if tarea_serializer.is_valid():
            tarea_serializer.save()
            tareas = Tarea.objects.filter(lista_kanban = tarea.lista_kanban, orden__gt=tarea.orden).order_by('orden')

            for t in tareas:
                t.orden = t.orden+1
                t.save()

            return Response(tarea_serializer.data, status=status.HTTP_200_OK)

        # return a meaningful error response
        return Response(tarea_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdjuntosApiView(APIView):

    def get(self, request, tarea_id):
        id_tarea = request.GET['adjunto_id']
        adjunto = Adjunto.objects.get(id=id_tarea)
        serializer = AdjuntoSerializer(adjunto)
        return Response(serializer.data)

    def post(self, request, tarea_id):
        archivo = request.FILES.get('adjunto')
        adjunto = Adjunto()
        adjunto.tarea = Tarea.objects.get(id=tarea_id)
        adjunto.archivo = archivo
        adjunto.tipo = archivo.content_type
        adjunto.nombre_archivo = archivo.name
        adjunto.autor = self.request.user
        adjunto.save()
        serializer = AdjuntoSerializer(adjunto)
        return Response(serializer.data)


class ComentariosApiView(APIView):

    def get(self, request):
        comentario_id = request.GET['comentario_id']
        comentario = Comentario.objects.get(id=comentario_id)
        serializer = AdjuntoSerializer(comentario)
        return Response(serializer.data)

    def post(self, request):
        tarea_id = request.POST['tarea_id']
        comentario_texto = request.POST['texto']
        comentario = Comentario()
        comentario.tarea = Tarea.objects.get(id=tarea_id)
        comentario.comentario = comentario_texto
        comentario.autor = self.request.user
        comentario.save()
        serializer = ComentarioSerializer(comentario)
        return Response(serializer.data)


class AsignacionListApiView(APIView):

    def post(self,request, tarea_id):
        usuario_id = request.data['usuario']
        asignacion = None
        try:
            asignacion = Asignacion.objects.get(tarea_id= tarea_id, usuario_id=usuario_id, activo=True)
            asignacion.activo = False
            asignacion.save()
        except:
            asignacion = Asignacion()
            asignacion.tarea = Tarea.objects.get(id= tarea_id)
            asignacion.usuario = User.objects.get(id= usuario_id)
            asignacion.usuario_asigna = self.request.user
            asignacion.save()
            
        serializer = AsignacionSerializer(asignacion)
        return Response(serializer.data)
    

class AsignacionApiView(APIView):

    def get (self, request, asignacion_id):
        pass

    def delete (self, reques, asignacion_id):
        pass

