from rest_framework import serializers
from proyectos.models import *
from kanban.serializers import *

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    usuario = AutorSerializer(many=False, read_only=True)

    class Meta:
        model = Equipo
        fields = ['usuario']