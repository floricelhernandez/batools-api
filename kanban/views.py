from django.views import generic
from kanban.models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
import json
import slack

# Serializadores.


class PrioridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridad
        fields = '__all__'


class AutorSerializer(serializers.ModelSerializer):
    perfil = serializers.SerializerMethodField()

    def get_perfil(self, obj):
        perfil = Perfil.objects.get(usuario_id=obj.id)
        serializer = PerfilSerializer(perfil)
        return serializer.data

    class Meta:
        model = User
        fields = ['username', 'email','perfil']


class AdjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjunto
        fields = '__all__'


class ComentarioSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(many=False, read_only=True)

    class Meta:
        model = Comentario
        fields = '__all__'


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = '__all__'


class AsignacionSerializer(serializers.ModelSerializer):
    usuario = AutorSerializer(many=False, read_only=True)

    class Meta:
        model = Asignacion
        fields = '__all__'


class TareaSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(many=False, read_only=True)
    prioridad = PrioridadSerializer(many=False, read_only=True)
    adjuntos = AdjuntoSerializer(many=True, read_only=True)
    #comentarios = ComentarioSerializer(many=True, read_only=True)
    comentarios = serializers.SerializerMethodField()

    def get_comentarios(self, instance):
        songs = Comentario.objects.filter(tarea_id=instance.id).order_by('-id')
        return ComentarioSerializer(songs, many=True).data

    class Meta:
        model = Tarea
        fields = '__all__'


# Vistas


class KanbanView(generic.ListView):
    template_name = 'kanban/kanban.html'
    context_object_name = 'listas'

    def get_queryset(self):
        return ListaKanban.objects.filter(sprint_id=self.kwargs['sprint_id']).order_by('orden')

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
        tarea.nombre =nombre
        tarea.lista_kanban= lista_kanban
        tarea.autor = self.request.user

        try:
            proyecto = Proyecto.objects.get(id=lista_kanban.sprint.proyecto.id)
            client = slack.WebClient(token=proyecto.slack_bot_token)
            client.chat_postMessage(
                channel="UUQCX554G",
                text="NUEVO: "+tarea.nombre+"! :tada:"
            )
        except:
            pass
        tarea.save()
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request, sprint_id):
        tarea_json = json.loads(request.POST['tarea'])
        tarea= Tarea.objects.get(id=tarea_json['id'])
        if tarea_json['prioridad'] is None:
            tarea.prioridad=None
        else:
            tarea.prioridad = Prioridad.objects.get(id=tarea_json['prioridad'])
        tarea.nombre = tarea_json['nombre']
        tarea.descripcion = tarea_json['descripcion']
        tarea.prioridad = Prioridad.objects.get(id=tarea_json['prioridad'])
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






