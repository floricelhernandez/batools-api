from django.shortcuts import render
from django.views import generic
from proyectos.models import *
from django import forms
from django.shortcuts import render
from kanban.models import *
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.


class ProyectoForm(forms.ModelForm):
    nombre = forms.CharField(widget= forms.TextInput
                           (attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.Textarea
                            (attrs={'class': 'form-control', "rows": 9}))
    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion',)


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ('usuario', 'rol',)
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }


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

        lista_por_hacer = ListaKanban()
        lista_por_hacer.sprint = sprint
        lista_por_hacer.nombre = "Por hacer"
        lista_por_hacer.estatus = Estatus.objects.get(clave='porhacer')
        lista_por_hacer.orden = 1
        lista_por_hacer.autor = self.request.user
        lista_por_hacer.save()

        lista_haciendo = ListaKanban()
        lista_haciendo.sprint = sprint
        lista_haciendo.nombre = "Haciendo"
        lista_haciendo.estatus = Estatus.objects.get(clave='haciendo')
        lista_haciendo.orden = 2
        lista_haciendo.autor = self.request.user
        lista_haciendo.save()

        lista_pruebas = ListaKanban()
        lista_pruebas.sprint = sprint
        lista_pruebas.nombre = "Pruebas"
        lista_pruebas.estatus = Estatus.objects.get(clave='enpruebas')
        lista_pruebas.orden = 3
        lista_pruebas.autor = self.request.user
        lista_pruebas.save()

        lista_hecho = ListaKanban()
        lista_hecho.sprint = sprint
        lista_hecho.nombre = "Hecho"
        lista_hecho.estatus = Estatus.objects.get(clave='hecho')
        lista_hecho.orden = 3
        lista_hecho.autor = self.request.user
        lista_hecho.save()

        equipos = Equipo.objects.filter(usuario=self.request.user)
        return render(request, 'kanban/proyectos.html', {'form': form, 'proyectos': equipos})


class EquipoView(LoginRequiredMixin,generic.View):
    def get(self, request, proyecto_id):
        form = EquipoForm()
        equipo = Equipo.objects.filter(proyecto_id=proyecto_id)
        return render(request, 'proyectos/equipo.html', {'equipo': equipo, 'form':form})

    def post(self, request, proyecto_id):
        equipo = EquipoForm(request.POST)
        equipo.instance.usuario_registra = self.request.user
        equipo.instance.proyecto = Proyecto.objects.get(id=proyecto_id)
        try:
            equipo.save()
        except IntegrityError as ex:
            messages.add_message(request, messages.ERROR, "Parece ser que el usuario que elegiste ya está en este proyecto.")

        form = EquipoForm()
        integrantes_equipo = Equipo.objects.filter(proyecto_id=proyecto_id)
        return render(request, 'proyectos/equipo.html', {'equipo': integrantes_equipo, 'form': form})