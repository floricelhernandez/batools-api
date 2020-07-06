from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from kanban.models import *
from kanban.serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from kanban.tasks import *


# Create your views here.
class TicketsView(LoginRequiredMixin,generic.ListView):
    template_name = 'ticktes/tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        proyectos = Equipo.objects.filter(usuario=self.request.user).values('proyecto_id')
        return Tarea.objects.filter(proyecto_id__in=proyectos, tipo_tarea__clave='ticket').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(TicketsView, self).get_context_data(**kwargs)
        context['prioridades'] = Prioridad.objects.all().order_by('orden')
        context['status'] = Estatus.objects.all()
        context['equipos'] = Equipo.objects.filter(usuario=self.request.user)
        proyectos = Equipo.objects.filter(usuario=self.request.user).values('proyecto_id')
        tareas = Tarea.objects.filter(proyecto_id__in=proyectos, tipo_tarea__clave='ticket')
        context['total_tickets'] = tareas.count()
        context['tickets_pendientes'] = tareas.exclude(lista_kanban__estatus__clave='hecho').count()
        context['tickets_cerrados'] = tareas.filter(lista_kanban__estatus__clave='hecho').count()
        context['tickets_archivados'] = tareas.filter(lista_kanban__estatus__clave='archivados').count()
        return context

class TicketApiView(APIView):

    def get(self, request, sprint_id):
        id_tarea = request.GET['idTarea']
        tarea = Tarea.objects.get(id=id_tarea)
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def post(self, request):
        proyecto_id = request.POST['proyecto']
        proyecto = Proyecto.objects.get(id=proyecto_id)
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion_aux']
        sprint = Sprint.objects.filter(proyecto_id=proyecto_id).order_by("-id")[0] # Obtenemos el sprint activo o el último creado
        try:
            lista_kanban = ListaKanban.objects.get(estatus__clave='sinpriorizar', sprint_id= sprint.id) # Asignar a la lista sin priorizar del sprint activo.
        except:
            lista_kanban = ListaKanban.objects.get(estatus__clave='porhacer',
                                                   sprint_id=sprint.id)  # Asignar a la lista sin priorizar del sprint activo.
        tarea = Tarea()
        tarea.nombre = nombre
        tarea.no_tarea = Tarea.objects.filter(proyecto_id=proyecto_id).count()+1
        tarea.proyecto = proyecto
        tarea.orden = 0
        tarea.autor = self.request.user
        tarea.tipo_tarea = TipoTarea.objects.get(clave='ticket')
        tarea.prioridad = Prioridad.objects.get(clave='ninguno')
        tarea.fijar_en_kanban = False
        tarea.save()

        arhivos = request.FILES.getlist('files')
        for archivo in arhivos:
            adjunto = Adjunto()
            adjunto.tarea = tarea
            adjunto.archivo = archivo
            adjunto.tipo = archivo.content_type
            adjunto.nombre_archivo = archivo.name
            adjunto.autor = self.request.user
            adjunto.save()

        try:
            if proyecto.slack_bot_token:
                if proyecto.slack_channel_id:
                    send_slack_message(proyecto.slack_bot_token, proyecto.slack_channel_id, self.request.user.username + " ha creado la tarea: " + tarea.nombre)
        except Exception as ex:
            print(ex)

        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request): #Actualizar estatus
        tarea= Tarea.objects.get(id=request.POST['tarea'])
        tarea.estatus = Estatus.objects.get(clave=request.POST['estatus'])
        tarea.save()
        data = {
            'pk': "ok",
        }
        return JsonResponse(data)

    def patch(self, request):
        tarea = Tarea.objects.get(id=request.POST['tarea'])
        sprint = Sprint.objects.filter(proyecto=tarea.proyecto).order_by("-id")[0]  # Obtenemos el sprint activo o el último creado
        try:
            lista_kanban = ListaKanban.objects.get(estatus=tarea.estatus, sprint_id=sprint.id, fijar_en_kanban=True)  # Asignar a la lista sin priorizar del sprint activo.
            tarea.lista_kanban = lista_kanban
            tarea.save()
            mensaje = "Se ha fijado el ticket en el Kanban en la lista" + lista_kanban.nombre
            success = True
        except:
            mensaje = "No existe una lista para el estatus " + tarea.estatus.descripcion + " en el Kanban. \n No se ha podido enviar."
            success = False

        data = {
            'success': success,
            'mensaje' : mensaje
        }
        return JsonResponse(data)

