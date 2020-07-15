from rest_framework import serializers
from proyectos.models import *
from kanban.serializers import *


class SprintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    sprints = serializers.SerializerMethodField()

    def get_sprints(self, obj):
        sprints = Sprint.objects.filter(proyecto_id=obj.id)
        serializer = SprintSerializer(sprints, many=True)
        return serializer.data

    class Meta:
        model = Proyecto
        fields = '__all__'


class EquipoSerializer(serializers.ModelSerializer):
    usuario = AutorSerializer(many=False, read_only=True)

    class Meta:
        model = Equipo
        fields = ['usuario']