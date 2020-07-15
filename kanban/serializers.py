from rest_framework import serializers
from kanban.models import *
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
    asignaciones = AsignacionSerializer(many=True)
    comentarios = serializers.SerializerMethodField()

    def get_comentarios(self, instance):
        coms = Comentario.objects.filter(tarea_id=instance.id).order_by('-id')
        return ComentarioSerializer(coms, many=True).data

    class Meta:
        model = Tarea
        fields = '__all__'


class ListasKanbanSerializar(serializers.ModelSerializer):
    tareas = serializers.SerializerMethodField()
    estatus_clave = serializers.SerializerMethodField()

    def get_tareas(self, instance):
        tareas = Tarea.objects.filter(lista_kanban=instance)
        return TareaSerializer(tareas, many=True).data

    def get_estatus_clave(self, instance):
        clave = Estatus.objects.get(id=instance.estatus.id)
        return clave.clave

    class Meta:
        model = ListaKanban
        fields = '__all__'
