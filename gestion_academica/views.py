"""
Vistas para el sistema de gestión académica.
Implementa separación de capas y control de acceso por roles.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View, TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.db.models import Q, Count
from django.core.exceptions import ValidationError
from django.http import Http404

from .models import Usuario, Carrera, Materia, Alumno, Inscripcion
from .forms import (
    LoginForm, CambiarPasswordForm, UsuarioForm, CarreraForm, 
    MateriaForm, AlumnoForm, InscripcionForm, FiltroMateriaForm,
    FiltroAlumnoMateriaForm
)
from .services import (
    UsuarioService, CarreraService, MateriaService, 
    AlumnoService, InscripcionService, ReportesService
)


# Mixins para control de acceso
class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere grupo de administrador"""
    def test_func(self):
        return (self.request.user.is_authenticated and 
                self.request.user.groups.filter(name='Administradores').exists())
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta página.')
        return redirect('gestion_academica:dashboard')


class AlumnoRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere grupo de alumno"""
    def test_func(self):
        return (self.request.user.is_authenticated and 
                self.request.user.groups.filter(name='Alumnos').exists())
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta página.')
        return redirect('gestion_academica:dashboard')


# === VISTAS DE AUTENTICACIÓN ===

class LoginView(View):
    """Vista para el login del sistema"""
    template_name = 'gestion_academica/auth/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('gestion_academica:dashboard')
        
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Verificar si es primer login
            if user.primer_login:
                messages.info(request, 'Debes cambiar tu contraseña en el primer acceso.')
                return redirect('gestion_academica:cambiar_password')
            
            messages.success(request, f'¡Bienvenido {user.first_name}!')
            return redirect('gestion_academica:dashboard')
        
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Vista para el logout del sistema"""
    def get(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('gestion_academica:login')


class CambiarPasswordView(LoginRequiredMixin, View):
    """Vista para cambiar contraseña en primer login"""
    template_name = 'gestion_academica/auth/cambiar_password.html'
    
    def get(self, request):
        if not request.user.primer_login:
            return redirect('gestion_academica:dashboard')
        
        form = CambiarPasswordForm(user=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if not request.user.primer_login:
            return redirect('gestion_academica:dashboard')
        
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('gestion_academica:dashboard')
        
        return render(request, self.template_name, {'form': form})


# === DASHBOARD PRINCIPAL ===

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista principal del dashboard según el grupo del usuario"""
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


# === GESTIÓN DE CARRERAS (Solo Admin) ===

class CarreraListView(AdminRequiredMixin, ListView):
    """Lista todas las carreras"""
    model = Carrera
    template_name = 'gestion_academica/carreras/list.html'
    context_object_name = 'carreras'
    paginate_by = 10
    
    def get_queryset(self):
        return Carrera.objects.filter(activa=True).order_by('nombre')


class CarreraCreateView(AdminRequiredMixin, CreateView):
    """Crea una nueva carrera"""
    model = Carrera
    form_class = CarreraForm
    template_name = 'gestion_academica/carreras/form.html'
    success_url = reverse_lazy('gestion_academica:carrera_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Carrera "{self.object.nombre}" creada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class CarreraUpdateView(AdminRequiredMixin, UpdateView):
    """Edita una carrera existente"""
    model = Carrera
    form_class = CarreraForm
    template_name = 'gestion_academica/carreras/form.html'
    success_url = reverse_lazy('gestion_academica:carrera_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Carrera "{self.object.nombre}" actualizada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class CarreraDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina una carrera"""
    model = Carrera
    template_name = 'gestion_academica/carreras/confirm_delete.html'
    success_url = reverse_lazy('gestion_academica:carrera_list')
    
    def delete(self, request, *args, **kwargs):
        try:
            carrera = self.get_object()
            CarreraService.eliminar_carrera(carrera.id)
            messages.success(request, f'Carrera "{carrera.nombre}" eliminada exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('gestion_academica:carrera_list')


# === GESTIÓN DE MATERIAS (Solo Admin) ===

class MateriaListView(AdminRequiredMixin, ListView):
    """Lista todas las materias con filtros"""
    model = Materia
    template_name = 'gestion_academica/materias/list.html'
    context_object_name = 'materias'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Materia.objects.filter(activa=True).select_related('carrera')
        
        # Filtro por carrera
        carrera_id = self.request.GET.get('carrera')
        if carrera_id:
            queryset = queryset.filter(carrera_id=carrera_id)
        
        return queryset.order_by('carrera__nombre', 'año', 'cuatrimestre', 'nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        return context


class MateriaCreateView(AdminRequiredMixin, CreateView):
    """Crea una nueva materia"""
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_academica/materias/form.html'
    success_url = reverse_lazy('gestion_academica:materia_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Materia "{self.object.nombre}" creada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class MateriaUpdateView(AdminRequiredMixin, UpdateView):
    """Edita una materia existente"""
    model = Materia
    form_class = MateriaForm
    template_name = 'gestion_academica/materias/form.html'
    success_url = reverse_lazy('gestion_academica:materia_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Materia "{self.object.nombre}" actualizada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class MateriaDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina una materia"""
    model = Materia
    template_name = 'gestion_academica/materias/confirm_delete.html'
    success_url = reverse_lazy('gestion_academica:materia_list')
    
    def delete(self, request, *args, **kwargs):
        try:
            materia = self.get_object()
            MateriaService.eliminar_materia(materia.id)
            messages.success(request, f'Materia "{materia.nombre}" eliminada exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('gestion_academica:materia_list')


# === GESTIÓN DE ALUMNOS (Solo Admin) ===

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
    success_url = reverse_lazy('gestion_academica:alumno_list')
    
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
    success_url = reverse_lazy('gestion_academica:alumno_list')
    
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
    success_url = reverse_lazy('gestion_academica:alumno_list')
    
    def delete(self, request, *args, **kwargs):
        try:
            alumno = self.get_object()
            nombre = alumno.nombre_completo
            alumno.delete()
            messages.success(request, f'Alumno "{nombre}" eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('gestion_academica:alumno_list')


# === GESTIÓN DE USUARIOS (Solo Admin) ===

class UsuarioListView(AdminRequiredMixin, ListView):
    """Lista todos los usuarios"""
    model = Usuario
    template_name = 'gestion_academica/usuarios/list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    
    def get_queryset(self):
        return Usuario.objects.filter(is_active=True).order_by('last_name', 'first_name')


class UsuarioCreateView(AdminRequiredMixin, CreateView):
    """Crea un nuevo usuario"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_academica/usuarios/form.html'
    success_url = reverse_lazy('gestion_academica:usuario_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Usuario "{self.object.get_full_name()}" creado exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class UsuarioUpdateView(AdminRequiredMixin, UpdateView):
    """Edita un usuario existente"""
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestion_academica/usuarios/form.html'
    success_url = reverse_lazy('gestion_academica:usuario_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Usuario "{self.object.get_full_name()}" actualizado exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    """Elimina un usuario"""
    model = Usuario
    template_name = 'gestion_academica/usuarios/confirm_delete.html'
    success_url = reverse_lazy('gestion_academica:usuario_list')
    
    def delete(self, request, *args, **kwargs):
        try:
            usuario = self.get_object()
            nombre = usuario.get_full_name()
            usuario.delete()
            messages.success(request, f'Usuario "{nombre}" eliminado exitosamente.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('gestion_academica:usuario_list')


# === GESTIÓN DE INSCRIPCIONES ===

class InscripcionListView(AdminRequiredMixin, ListView):
    """Lista todas las inscripciones"""
    model = Inscripcion
    template_name = 'gestion_academica/inscripciones/list.html'
    context_object_name = 'inscripciones'
    paginate_by = 10
    
    def get_queryset(self):
        return Inscripcion.objects.filter(activa=True).select_related('alumno', 'materia').order_by('-fecha_inscripcion')


class InscripcionCreateView(AdminRequiredMixin, CreateView):
    """Crea una nueva inscripción"""
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'gestion_academica/inscripciones/form.html'
    success_url = reverse_lazy('gestion_academica:inscripcion_list')
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Inscripción creada exitosamente.')
            return response
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class InscripcionBajaView(AdminRequiredMixin, View):
    """Da de baja una inscripción"""
    def post(self, request, pk):
        try:
            inscripcion = InscripcionService.dar_de_baja_inscripcion(pk)
            messages.success(request, f'Inscripción dada de baja exitosamente.')
        except ValidationError as e:
            messages.error(request, str(e))
        
        return redirect('gestion_academica:inscripcion_list')


# === VISTAS ESPECÍFICAS PARA ALUMNOS ===

class MisMateriaView(AlumnoRequiredMixin, TemplateView):
    """Vista para que el alumno vea sus materias"""
    template_name = 'gestion_academica/alumno/mis_materias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            alumno = self.request.user.alumno
            context['alumno'] = alumno
            context['inscripciones'] = InscripcionService.obtener_inscripciones_alumno(alumno.id)
        except:
            messages.error(self.request, 'No se encontró información del alumno.')
        
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


class InscribirseView(AlumnoRequiredMixin, View):
    """Vista para que el alumno se inscriba a una materia"""
    def post(self, request, materia_id):
        try:
            alumno = request.user.alumno
            inscripcion = InscripcionService.inscribir_alumno(alumno.id, materia_id)
            messages.success(request, f'Te has inscripto exitosamente a {inscripcion.materia.nombre}.')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error al procesar la inscripción.')
        
        return redirect('gestion_academica:oferta_academica')


# === VISTAS PARA INVITADOS ===

class CarrerasPublicasView(TemplateView):
    """Vista pública de carreras (para invitados)"""
    template_name = 'gestion_academica/publico/carreras.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carreras'] = Carrera.objects.filter(activa=True).order_by('nombre')
        return context


class MateriasPublicasView(TemplateView):
    """Vista pública de materias (para invitados)"""
    template_name = 'gestion_academica/publico/materias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtro por carrera
        carrera_id = self.request.GET.get('carrera')
        materias = Materia.objects.filter(activa=True).select_related('carrera')
        
        if carrera_id:
            materias = materias.filter(carrera_id=carrera_id)
        
        context['materias'] = materias.order_by('carrera__nombre', 'año', 'cuatrimestre', 'nombre')
        context['filtro_form'] = FiltroMateriaForm(self.request.GET or None)
        
        return context


# === FILTROS Y CONSULTAS FUNCIONALES ===

class MateriasPorCarreraView(LoginRequiredMixin, TemplateView):
    """Vista para filtrar materias por carrera"""
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
    """Vista para ver alumnos inscritos en una materia"""
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
        
        # Formulario para seleccionar materia
        context['materias'] = Materia.objects.filter(activa=True).select_related('carrera')
        
        return context


class MateriasConCupoView(LoginRequiredMixin, TemplateView):
    """Vista para ver materias con cupo disponible"""
    template_name = 'gestion_academica/filtros/materias_con_cupo.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materias'] = MateriaService.obtener_materias_con_cupo()
        return context


# === REPORTES ===

class ReportesView(AdminRequiredMixin, TemplateView):
    """Vista de reportes generales"""
    template_name = 'gestion_academica/reportes/general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte'] = ReportesService.reporte_general()
        context['materias_por_carrera'] = ReportesService.materias_con_cupo_por_carrera()
        return context
