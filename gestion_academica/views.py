from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError

from carrera.models import Carrera
from inscripcion.models import Inscripcion
from inscripcion.services import InscripcionService
from materia.models import Materia
from materia.services import MateriaService
from usuario.views import AdminRequiredMixin, AlumnoRequiredMixin

from .services import ReportesService
from .forms import FiltroMateriaForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion_academica/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['user'] = user
        
        if user.groups.filter(name='Administradores').exists():
            context['reporte'] = ReportesService.reporte_general()
        elif user.groups.filter(name='Alumnos').exists():
            try:
                alumno = user.alumno
                context['alumno'] = alumno
                context['inscripciones'] = InscripcionService.obtener_inscripciones_alumno(alumno.id)
            except:
                messages.error(self.request, 'No se encontró información del alumno.')
        
        return context


class CarrerasPublicasView(TemplateView):
    template_name = 'gestion_academica/publico/carreras.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carreras'] = Carrera.objects.filter(activa=True).order_by('nombre')
        return context


class MateriasPublicasView(TemplateView):
    template_name = 'gestion_academica/publico/materias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carrera_id = self.request.GET.get('carrera')
        materias = Materia.objects.filter(activa=True).select_related('carrera')
        
        if carrera_id:
            materias = materias.filter(carrera_id=carrera_id)
        
        context['materias'] = materias.order_by('carrera__nombre', 'año', 'cuatrimestre', 'nombre')
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        
        return context


class MateriasPorCarreraView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion_academica/filtros/materias_por_carrera.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carrera_id = self.request.GET.get('carrera')
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        
        if carrera_id:
            try:
                context['materias'] = MateriaService.obtener_materias_por_carrera(carrera_id)
                context['carrera_seleccionada'] = Carrera.objects.get(id=carrera_id)
            except ValidationError as e:
                messages.error(self.request, str(e))
        
        return context


class AlumnosPorMateriaView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion_academica/filtros/alumnos_por_materia.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        materia_id = self.request.GET.get('materia')
        
        if materia_id:
            try:
                context['inscripciones'] = InscripcionService.obtener_alumnos_materia(materia_id)
                context['materia_seleccionada'] = Materia.objects.get(id=materia_id)
            except ValidationError as e:
                messages.error(self.request, str(e))
        
        context['materias'] = Materia.objects.filter(activa=True).select_related('carrera')
        
        return context


class MateriasConCupoView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion_academica/filtros/materias_con_cupo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materias'] = MateriaService.obtener_materias_con_cupo()
        return context


class ReportesView(AdminRequiredMixin, TemplateView):
    template_name = 'gestion_academica/reportes/general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte'] = ReportesService.reporte_general()
        context['materias_por_carrera'] = ReportesService.materias_con_cupo_por_carrera()
        return context

class OfertaAcademicaView(AlumnoRequiredMixin, TemplateView):
    """Vista para que el alumno vea la oferta académica de su carrera"""
    template_name = 'gestion_academica/alumno/oferta_academica.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            alumno = self.request.user.alumno
            context['alumno'] = alumno
            context['materias'] = MateriaService.obtener_materias_por_carrera(alumno.carrera.id)
            
            # Materias en las que ya está inscripto
            inscripciones = Inscripcion.objects.filter(alumno=alumno, activa=True)
            context['materias_inscripto'] = [i.materia.id for i in inscripciones]
            
        except Exception as e:
            messages.error(self.request, 'No se pudo cargar la oferta académica.')
        
        return context
