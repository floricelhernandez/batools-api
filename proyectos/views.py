from django.shortcuts import render
from django.views import generic
from proyectos.models import *
from django import forms
from django.shortcuts import render
from kanban.models import *
from django.db import transaction

# Create your views here.


class ProyectoForm(forms.ModelForm):

    nombre = forms.CharField(widget= forms.TextInput
                           (attrs={'class': 'form-control', "rows": 4}))
    descripcion = forms.CharField(widget=forms.Textarea
                            (attrs={'class': 'form-control'}))

    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion',)


class IndexView(generic.View):

    def get(self, request):
        form = ProyectoForm()
        proyectos = Proyecto.objects.order_by('nombre')
        return render(request, 'kanban/proyectos.html', {'form': form, 'proyectos': proyectos})

    @transaction.atomic()
    def post(self, request):
        proyecto = ProyectoForm(request.POST)
        proyecto.instance.autor = self.request.user
        proyecto.save()
        form = ProyectoForm()
        proyectos = Proyecto.objects.order_by('nombre')

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

        lista_hecho = ListaKanban()
        lista_hecho.sprint = sprint
        lista_hecho.nombre = "Hecho"
        lista_hecho.estatus = Estatus.objects.get(clave='hecho')
        lista_haciendo.orden = 3
        lista_hecho.autor = self.request.user
        lista_hecho.save()

        return render(request, 'kanban/proyectos.html', {'form': form, 'proyectos': proyectos})


class ProyectoView(generic.View):

    def post(self):
        pass