from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.core.exceptions import ValidationError

from usuario.views import AdminRequiredMixin

from .models import Alumno
from .forms import AlumnoForm
# Create your views here.

class AlumnoListView(AdminRequiredMixin, ListView):
    """Lista todos los alumnos"""
    model = Alumno
    template_name = 'gestion_academica/alumnos/list.html'
    context_object_name = 'alumnos'
    paginate_by = 10
    
    def get_queryset(self):
        return Alumno.objects.filter(activo=True).select_related('carrera', 'usuario').order_by('usuario__last_name', 'usuario__first_name')


class AlumnoDetailView(AdminRequiredMixin, DetailView):
    """Muestra los detalles de un alumno"""
    model = Alumno
    template_name = 'gestion_academica/alumnos/detail.html'
    context_object_name = 'object'
    
    def get_queryset(self):
        return Alumno.objects.select_related('carrera', 'usuario').prefetch_related(
            'inscripciones__materia', 'usuario__groups'
        )


class AlumnoCreateView(AdminRequiredMixin, CreateView):
    """Crea un nuevo alumno"""
    model = Alumno
    form_class = AlumnoForm
    template_name = 'gestion_academica/alumnos/form.html'
    success_url = reverse_lazy('alumno_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Alumno "{self.object.nombre_completo}" creado exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class AlumnoUpdateView(AdminRequiredMixin, UpdateView):
    """Edita un alumno existente"""
    model = Alumno
    form_class = AlumnoForm
    template_name = 'gestion_academica/alumnos/form.html'
    success_url = reverse_lazy('alumno_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Alumno "{self.object.nombre_completo}" actualizado exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class AlumnoDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina un alumno"""
    model = Alumno
    template_name = 'gestion_academica/alumnos/confirm_delete.html'
    success_url = reverse_lazy('alumno_list')
    
    def delete(self, request, *args, **kwargs):
        try:
            alumno = self.get_object()
            nombre = alumno.nombre_completo
            alumno.delete()
            messages.success(request, f'Alumno "{nombre}" eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('alumno_list')
