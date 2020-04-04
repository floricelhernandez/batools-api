from django.shortcuts import render
from django.views import generic
from kanban.models import *


# Create your views here.
class TicketsView(generic.ListView):
    template_name = 'ticktes/tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Tarea.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TicketsView, self).get_context_data(**kwargs)
        context['prioridades'] = Prioridad.objects.all().order_by('orden')
        return context
