from django.views import generic
from kanban.models import *
from .tasks import *
from kanban.serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.contrib.auth.mixins import LoginRequiredMixin


class KanbanView(LoginRequiredMixin, generic.ListView):
    template_name = 'kanban/kanban.html'
    context_object_name = 'listas'

    def get_queryset(self):
        return ListaKanban.objects.filter(sprint_id=self.kwargs['sprint_id'], fijar_en_kanban=True).order_by('orden')

    def get_context_data(self, **kwargs):
        context = super(KanbanView, self).get_context_data(**kwargs)
        context['prioridades'] = Prioridad.objects.all().order_by('orden')
        sprint = Sprint.objects.get(id=self.kwargs['sprint_id'])
        context['equipo'] = Equipo.objects.filter(proyecto_id=sprint.proyecto.id)
        return context


class TareaApiView(APIView):

    def get(self, request, sprint_id):
        id_tarea = request.GET['idTarea']
        tarea = Tarea.objects.get(id=id_tarea)
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def post(self, request, sprint_id):
        mover_a = request.POST['moverA']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        lista_kanban = ListaKanban.objects.get(estatus__clave=mover_a, sprint_id=sprint_id)
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

    def patch(self, request, sprint_id):
        mover_a = request.POST['moverA']
        id_tarea = request.POST['idTarea']
        lista_kanban = ListaKanban.objects.get(estatus__clave=mover_a, sprint_id=sprint_id)
        tarea = Tarea.objects.get(id=id_tarea)
        tarea.lista_kanban = lista_kanban
        tarea.estatus = lista_kanban.estatus
        tarea.save()
        data = {
            'pk': "ok",
        }
        return JsonResponse(data)


class AdjuntosApiView(APIView):

    def get(self, request):
        id_tarea = request.GET['adjunto_id']
        adjunto = Adjunto.objects.get(id=id_tarea)
        serializer = AdjuntoSerializer(adjunto)
        return Response(serializer.data)

    def post(self, request):
        id_tarea = request.POST['tarea_id']
        archivo = request.FILES.get('adjunto')
        adjunto = Adjunto()
        adjunto.tarea = Tarea.objects.get(id=id_tarea)
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


class AsignacionApiView(APIView):

    def post(self,request):
        tarea_id = request.POST['tarea_id']
        usuario_id = request.POST['usuario_id']
        asignacion = None
        try:
            asignacion = Asignacion.objects.get(tarea_id= tarea_id, usuario_id=usuario_id, activo=True)
        except:
            pass
        if asignacion is None:
            asignacion = Asignacion()
            asignacion.tarea = Tarea.objects.get(id= tarea_id)
            asignacion.usuario = User.objects.get(id= usuario_id)
            asignacion.usuario_asigna = self.request.user
            asignacion.save()
        else:
            asignacion.activo = False
            asignacion.save()

        serializer = AsignacionSerializer(asignacion)
        return Response(serializer.data)










